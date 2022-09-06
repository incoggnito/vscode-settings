import streamlit as st
import numpy as np
import pandas as pd
import holidays
from datetime import datetime
from app.core.auth import Session
from app.core.api import post, get
from app.pages.calendar import load_cal_by_sql, string2date_tz
from app.core.config import (
    LAW,
    LAW_ANUE_BMW,
    SPECIAL_PROJECTS,
    DAY_ABBR,
    WEEKDAYS,
    VIEW,
    SPECIAL_Tags,
)


def get_special_events(df: pd.DataFrame) -> pd.DataFrame:
    df["Abwesenheit"] = ""
    for key, idx in SPECIAL_PROJECTS.items():
        df.loc[df.project_def_id == idx, "Abwesenheit"] = key
    return df


def get_holidays(df: pd.DataFrame, province: str, year: int) -> pd.DataFrame:
    g = holidays.Germany(years=year, prov=province)
    df.loc[df.startdate.dt.date.isin(list(g.keys())), "Abwesenheit"] = "F"
    return df


def split_long_days(df: pd.DataFrame) -> pd.DataFrame:
    long_days = df.loc[(df.duration / 24) > 1]
    rows = []
    for _, row in long_days.iterrows():
        for i in range(int(row.duration / 24)):
            row["startdate"] = row["startdate"] + (i * pd.Timedelta(1, unit="d"))
            row["enddate"] = row["startdate"] + ((i + 1) * pd.Timedelta(1, unit="d"))
            rows.append(row)
    # df = pd.concat(df, pd.DataFrame(rows))
    df = pd.concat([df, pd.DataFrame(rows)], axis=0)
    df.drop(long_days.index.values, inplace=True, errors="ignore")

    return df


def timedelta_to_hour_min(s: pd.Series):
    s = s.replace(pd.NaT, pd.Timedelta(0, unit="h"))
    minus = s.dt.total_seconds() < 0
    s[minus] = abs(s[minus])
    tc = s.dt.components
    tc["fullhours"] = tc["days"] * 24 + tc["hours"]
    tc = tc[["fullhours", "minutes"]].astype(str)
    s = tc.fullhours.str.zfill(2) + ":" + tc.minutes.str.zfill(2)
    s[s == "00:00"] = ""
    s[minus] = "-" + s[minus]
    return s


def replace_intervals(column: pd.Series, intervals: dict) -> pd.Series:
    """Replace values in ranges in a pandas Series by any object

    Args:
        intervals (List): Dict containing tuples or list with ranges and replacement (from, to, value to replace)
        column (pd.Series): The pandas column target

    Returns:
        pd.Series: A pandas series containing the replaced values
    """
    intervals = pd.DataFrame.from_dict(intervals, "index").reset_index()
    intervals = intervals.set_index(
        pd.IntervalIndex.from_arrays(left=intervals[0], right=intervals[1], closed="left")
    )["index"]

    return column.map(intervals)


def floathour_to_timedelta(s: pd.Series):
    s = s.fillna(0)
    return (s * 60).astype("timedelta64[m]")


def datetime_to_timedelta(s: pd.Series):
    return pd.to_timedelta(pd.to_datetime(s).dt.minute / 60, unit="hours")


def set_index_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df["Datum"] = df.index.values
    df.Datum = pd.to_datetime(df.Datum) + pd.Timedelta(1, unit="d")
    return df.set_index("Datum", drop=True)


def drop_pause_begin_or_end_of_day(
    df: pd.DataFrame,
) -> pd.DataFrame:  # TODO Clean this code
    pdi_end_of_day = df.loc[:, ["id", "project_def_id"]].groupby(df.startdate.dt.floor("D")).last()
    pdi_start_of_day = df.loc[:, ["id", "project_def_id"]].groupby(df.startdate.dt.floor("D")).first()
    idx_end_of_day_errs = pdi_end_of_day[pdi_end_of_day.project_def_id == 9].id.to_list()
    idx_start_of_day_errs = pdi_start_of_day[pdi_start_of_day.project_def_id == 9].id.to_list()
    pause_errs = idx_start_of_day_errs + idx_end_of_day_errs
    df = df[~df.id.isin(pause_errs)]

    return df


def get_cal_entries(calendar: pd.DataFrame, date_index: pd.Series) -> pd.DataFrame:
    details = calendar.loc[date_index, ["summary", "startdate", "enddate"]]
    details["Beginn"] = details.startdate.dt.time.astype(str)
    details["Ende"] = details.enddate.dt.time.astype(str)
    details["Betreff"] = details.summary
    return details.loc[:, ["Betreff", "Beginn", "Ende"]]


def workinghours_view(
    data: pd.DataFrame,
    workdays: list,
    trans_day: dict,
    dayhours: int,
    session_var: Session,
    anue: bool = False,
) -> pd.DataFrame:
    """Create a new daily table view"""

    # Remove dayborder pause errs
    df = drop_pause_begin_or_end_of_day(data)
    data.index = data.startdate.dt.date

    # Remove half day holiday
    half_day_vac = df[(df.Abwesenheit == "U") & (df.duration == (dayhours / 2))]
    df = df.drop(index=half_day_vac.index)

    # TODO test if it works. keep or remove, respectively
    df = df.sort_values(by="startdate")

    # Split pause into a new dataframe
    pause = df[df.project_def_id == 9]
    df = df[df.project_def_id != 9]

    pause = set_index_to_datetime(pause.groupby(pause.startdate.dt.floor("D")).sum())

    # sum working hours of each day
    Work_hours_a_day = set_index_to_datetime(df.groupby(df.startdate.dt.floor("D")).sum())

    # calculate the beginning and the end of day
    f, l = "first", "last"
    df = set_index_to_datetime(
        df.groupby(df["startdate"].dt.floor("D"))
        .agg([l, f])
        .loc[:, [("Abwesenheit", f), ("startdate", f), ("enddate", l)]]
    )
    df = df.droplevel(level=1, axis=1)

    # Pausenzeiten
    pause_ranges_anue = {0: (0, 4.5), 0.25: (4.5, 6), 1: (6, 15)}
    pause_ranges = {0: (0, 6), 0.5: (6, 9), 0.75: (9, 15)}

    df["daily_worktime"] = Work_hours_a_day.duration

    if anue:
        df["pause_by_law_dec"] = replace_intervals(df.daily_worktime, pause_ranges_anue)
    else:
        df["pause_by_law_dec"] = replace_intervals(df.daily_worktime, pause_ranges)

    df["pause_dec"] = pause.duration

    # Check gaps
    df["duration"] = (df.enddate - df.startdate).astype("timedelta64[m]") / 60
    # Remove duration and worktime on days longer then 20 hours
    df.loc[df.duration > 20, ["duration", "daily_worktime"]] = np.nan
    df["worktime_dec"] = df.duration - df.pause_dec
    wtimes = df[["worktime_dec", "daily_worktime"]].dropna()
    gaps = wtimes[wtimes.iloc[:, 0] > wtimes.iloc[:, 1]]
    duplicates = wtimes[wtimes.iloc[:, 0] < wtimes.iloc[:, 1]]

    stop_view = False

    if not gaps.empty:
        st.error("Achtung! An folgenden Tagen gibt es noch Lücken im Kalender:")
        gap_date_index = gaps.index.to_series().dt.date.values
        gaps.columns = ["Start-End-Pause", "Ticket-Dauer-Summe"]
        gaps.index = gap_date_index
        st.write(gaps)
        stop_view = True
        with st.expander("Mehr Details zu den erfassten Tickets aus dem Kalender anzeigen"):
            st.write(get_cal_entries(calendar=data, date_index=gap_date_index))

    if not duplicates.empty:
        st.error("Achtung! An folgenden Tagen gibt es noch doppelte Einträge im Kalender:")
        duplicate_date_index = duplicates.index.to_series().dt.date.values
        duplicates.columns = ["Start-End-Pause", "Ticket-Dauer-Summe"]
        duplicates.index = duplicate_date_index
        st.write(duplicates)
        st.info("Doppelte Einträge sind nicht zulässig!")
        stop_view = True
        with st.expander("Mehr Details zu den erfassten Tickets aus dem Kalender anzeigen"):
            st.write(get_cal_entries(calendar=data, date_index=duplicate_date_index))

    if stop_view:
        st.stop()

    # calculate additional pause and flextime
    df["add_pause_dec"] = df.pause_dec - df.pause_by_law_dec
    to_less_pause_idx = df.add_pause_dec < 0
    no_pause_idx = df.worktime_dec.isnull() & df.startdate.notnull()
    df.worktime_dec.loc[no_pause_idx] = df.daily_worktime
    idx = to_less_pause_idx + no_pause_idx
    df.pause_dec[idx] = df.pause_by_law_dec[idx]
    df["flextime"] = df.worktime_dec - dayhours
    df.flextime.loc[to_less_pause_idx] = df.flextime + df.add_pause_dec
    df.add_pause_dec.loc[to_less_pause_idx] = 0
    df = df.set_index(df.index.to_series().dt.date)

    df.flextime[half_day_vac.startdate.dt.date] = df.flextime[half_day_vac.startdate.dt.date] + (dayhours / 2)

    # Fill missing calendar days
    df.Abwesenheit.loc[half_day_vac.startdate.dt.date] = "1/2 U"
    df.loc[df.Abwesenheit == "F", ["startdate", "enddate"]] = np.nan
    df = df.asfreq("D", method=None, fill_value=np.nan)
    g = holidays.Germany(years=session_var.year, prov=session_var.province)
    df.loc[df.index.to_series().dt.date.isin(list(g.keys())), "Abwesenheit"] = "F"

    # Add calendar week
    df["KW"] = df.index.to_series().dt.isocalendar().week.astype(str)
    df.loc[df.KW.duplicated(), "KW"] = ""
    df["Wochentag"] = pd.Series(df.index.values).dt.day_name().replace(trans_day).to_list()

    # filter by workdays
    df = df[df.Wochentag.isin(workdays)]

    # convert to timedelta
    df["worktime"] = floathour_to_timedelta(df.worktime_dec)
    df["add_pause"] = floathour_to_timedelta(df.add_pause_dec)
    df["pause"] = floathour_to_timedelta(df.pause_by_law_dec)

    # convert to datetime
    df["Arbeitszeit"] = timedelta_to_hour_min(df.worktime)
    df["Pause"] = timedelta_to_hour_min(df.pause)
    df["Zusatzpause"] = timedelta_to_hour_min(df.add_pause)

    # Arbeitszeiten View
    df["Arbeitsbeginn"] = df.startdate.dt.strftime("%H:%M")
    df["Arbeitsende"] = df.enddate.dt.strftime("%H:%M")
    df["duration"] = (df.enddate - df.startdate).astype("timedelta64[m]") / 60
    df["Überstunden"] = timedelta_to_hour_min(floathour_to_timedelta(df.flextime))

    # Hide nan values in streamlit dataframe
    df.Abwesenheit = df.Abwesenheit.fillna("")
    df.Arbeitsende = df.Arbeitsende.fillna("")
    df.Arbeitsbeginn = df.Arbeitsbeginn.fillna("")
    df.Pause = df.Pause.fillna("")
    df.loc[
        df.Abwesenheit.isin(list(SPECIAL_PROJECTS.keys())),
        ["Arbeitsbeginn", "Arbeitsende", "Überstunden", "Arbeitszeit", "Zusatzpause"],
    ] = ""

    df.index = pd.Series(df.index).dt.strftime("%d.%m.%Y")

    return df


def special_days(df: pd.DataFrame) -> pd.Series:
    s = df.groupby(df.Abwesenheit).count()["KW"][1:]
    if not "U" in list(s.keys()):
        s["U"] = 0

    if "1/2 U" in list(s.keys()):
        s.U = s.U + (0.5 * s["1/2 U"])
        s = s.drop("1/2 U")

    s.index = [SPECIAL_Tags[v] for v in s.index]
    s.name = "Anzahl"
    return s


def format_df(df: pd.DataFrame) -> pd.DataFrame:
    df = string2date_tz(df)
    df.project_def_id = df.project_def_id.astype(int)
    return df


# @st.cache(allow_output_mutation=True)
def calc_specialdays(df: pd.DataFrame, province: str, year: int, month: int) -> pd.DataFrame:

    df = split_long_days(df)
    df = get_special_events(df)
    df = get_holidays(df, province, year)
    return df


def app() -> None:
    """Run a workinghours app"""

    s = Session()
    st.title("🕚 Stundenabrechnung ")

    if "last_month_vacation" in s.__dict__:
        dailyhours = s.workhours / s.workdays
        st.write(f"Die Sollstunden von **{s.name}** betragen **{dailyhours} h** am Tag.")

        col1, col2 = st.columns(2)

        s = Session()

        if "ANUE" in s.groups:
            anue = True
            col2.write(LAW_ANUE_BMW)
        else:
            anue = False
            col2.write(LAW)

        workdays = col1.multiselect(
            "Arbeitstage",
            DAY_ABBR,
            default=DAY_ABBR[:-2],
        )

        trans_day = dict(zip(WEEKDAYS, DAY_ABBR))

        df = load_cal_by_sql(s.uid, s.year, s.month)
        if df.empty:
            st.error("Kalendereintrag in Datenbank nicht vorhanden!")
        else:
            formated_df = format_df(df)
            projecthours = calc_specialdays(formated_df, s.province, s.year, s.month)
            workinghours = workinghours_view(
                projecthours,
                anue=anue,
                workdays=workdays,
                trans_day=trans_day,
                dayhours=dailyhours,
                session_var=s,
            )
            st.table(workinghours.loc[:, VIEW])

            col3, col4, _, col6 = st.columns(4)
            sdays = special_days(workinghours)

            if len(sdays):
                col3.write(sdays)
                used_vacation = s.vacation + s.rest_vacation_last_year - s.last_month_vacation
                used_vacation += sdays.Urlaub

            rest_vacation = s.vacation + s.rest_vacation_last_year - used_vacation

            vacation_overview = pd.Series(
                {
                    f"U-Anspruch ({s.year})": f"{s.vacation}",
                    f"Resturlaub ({s.year -1})": f"{s.rest_vacation_last_year}",
                    "genommene U-Tage": f"{used_vacation}",
                    "Resturlaub": f"{rest_vacation}",
                },
                name="Tage",
            )
            col4.write(vacation_overview)

            flex_cur_month = workinghours.flextime.sum()
            flex_all_month = s.flextime + flex_cur_month
            flex = pd.Series(
                {
                    "Vormonat": s.flextime,
                    "Aktuell": flex_cur_month,
                    "Gesamt": flex_all_month,
                },
            )

            flex_str = timedelta_to_hour_min(floathour_to_timedelta(flex))
            flex_str.name = "Überstunden"
            col6.write(flex_str)

            # Check if month is already saved and if its next month begin
            if (not get(f"monthly/{s.year}/{s.month}")["month"] == s.month) or (
                not datetime.now() > datetime(s.year, s.month + 1, 3)
            ):
                if st.button("Speichern"):
                    data = {
                        "year": s.year,
                        "month": s.month,
                        "vacation": rest_vacation,
                        "flextime": flex_all_month,
                        "submitter_id": s.uid,
                    }
                    get(f"meta{s.last_valid_month}")
                    post("monthly", data=data)
                    st.success("Saved to database!")
            else:
                st.info(
                    "Die Stundenabrechnung wurde bereits gespeichert! Änderungen sind aktuell nicht mehr möglich, da der Abrechnungszeitraum bereits begonnen hat. Bei Fehlern bitte beim Personalverantwortlichen anfragen."
                )
    else:
        st.error("Die Stundenabrechnung des vorherigen Monats fehlt noch. Bitte zuerst absenden!")

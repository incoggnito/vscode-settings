import calendar
import difflib
import logging
from ast import literal_eval
from datetime import date, datetime, time, timedelta
from typing import Optional, Union

import caldav
import pandas as pd
import pytz
import streamlit as st

from icalendar import Event
from app.core.api import delete, get, post
from app.core.auth import Session, decrypt_password, state

LOGGER = logging.getLogger(__file__)


def string2date_tz(data: pd.DataFrame, timeformat: str = "%m/%d/%Y %H:%M", tz: str = "Europe/Berlin") -> pd.DataFrame:
    mytimezone = pytz.timezone(tz)
    data.startdate = pd.to_datetime(data.startdate, utc=True)
    data.enddate = pd.to_datetime(data.enddate, utc=True)
    data.startdate = pd.to_datetime(data.startdate.dt.tz_convert(mytimezone), format=timeformat)
    data.enddate = pd.to_datetime(data.enddate.dt.tz_convert(mytimezone), format=timeformat)
    return data


class MyCalendar:
    """Connect to a caldav calendar"""

    def __init__(self, url: str):
        self.url = url.lower()

    def connect_server(self, user: str, password: str) -> None:
        """Connect to an caldav server, get logged-in principal and all calendars"""
        try:
            self.client = caldav.DAVClient(self.url, username=user, password=password)
        except:
            st.error("Zugangsdaten zur Nextcloud fehlerhaft!")
            st.stop()
        self.principal = self.client.principal()
        self.calendars = self.principal.calendars()

    def get_calendar(self, name: str = "") -> None:
        """Select a specific calendar"""
        if name:
            self.calendar = [cal for cal in self.calendars if f"{name}/" in str(cal)][0]
        else:
            if len(self.calendars) > 0:
                self.calendar = self.calendars[0]

    def create_event(self, start: datetime, end: datetime, summary: str) -> None:
        start = start.to_pydatetime()
        end = end.to_pydatetime()
        e = Event()
        e.add("summary", summary)
        e.add("dtstart", start)
        e.add("dtend", end)
        self.calendar.save_event(e)

    def get_events_in_timerange(
        self,
        start: datetime = datetime(2021, 1, 1),
        end: datetime = datetime(2024, 1, 1),
    ) -> None:
        """Get all events in a time range

        Args:
            startdate (datetime, optional): Start date. Defaults to datetime(2021, 1, 1).
            enddate (datetime, optional): End date. Defaults to datetime(2024, 1, 1).
        """ "Get all events between two dates"
        self.events = self.calendar.date_search(start, end, expand=True)

    def get_events(self) -> None:
        """Get all events from a certain calendar"""
        self.events = self.calendar.events()

    @staticmethod
    def _format_datetime(dt: Union[datetime, date], add_time: time) -> datetime:
        try:
            if str(type(dt)) == "<class 'datetime.date'>":
                if add_time == time(22, 59):
                    dt = datetime.combine(dt - timedelta(days=1), add_time, pytz.timezone("UTC"))
                else:
                    dt = datetime.combine(dt, add_time, pytz.timezone("UTC"))

            if not dt.tzname():
                dt = dt.astimezone(pytz.timezone("UTC"))
        except:
            LOGGER.error("Time {dt} occurs errors")

        return dt

    def get_data_from_events(self) -> pd.DataFrame:
        """Select data from calender events

        Returns:
            pd.DataFrame: Return a table of events
        """
        data: dict = {"summary": [], "startdate": [], "enddate": []}
        for eventraw in self.events:
            try:
                e = eventraw.instance.vevent
                eventraw.load()
                data["summary"].append(e.summary.value)
                data["startdate"].append(self._format_datetime(e.dtstart.value, time(0, 0)))
                data["enddate"].append(self._format_datetime(e.dtend.value, time(22, 59)))
            except:
                LOGGER.error(f"The calendar event is not readable: {e}")
                continue

        return self._format_data(pd.DataFrame(data))

    @staticmethod
    def _format_data(data: pd.DataFrame) -> pd.DataFrame:
        data = string2date_tz(data)
        data["duration"] = (data.enddate - data.startdate).astype("timedelta64[m]") / 60
        data.sort_values(by="startdate", inplace=True)
        data = data.reset_index(drop=True)
        data.index = [i for i in range(len(data))]
        return data


def get_year() -> int:
    """Get the current year

    Returns:
        int: The current year
    """
    return int(datetime.today().year)


def get_month() -> int:
    """Get the current month

    Returns:
        int: The current month
    """
    return int(datetime.today().month)


def get_last_month_day(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


# cache decorator misplaced
# @st.cache(allow_output_mutation=True)
def get_calendar_data(user_id: int, month: int, year: int, cal_name: str, *args) -> pd.DataFrame:
    """Load calender data from nextcloud caldav"""
    base_url = f"https://cloud.amitronics.net/remote.php/dav/calendars/{args[0]}/{cal_name}/"
    cal = MyCalendar(base_url)
    cal.connect_server(args[0], args[1])
    idx_tags = {k.lower(): v for k, v in args[2].items()}
    cal.get_calendar(cal_name.lower())
    last_month_day = get_last_month_day(year, month)
    cal.get_events_in_timerange(
        datetime(year, month, 1, 0, 0),
        datetime(year, month, last_month_day, 23, 59),
    )
    df = cal.get_data_from_events()
    if not df.empty:
        df.summary = df.summary.str.replace("[", "", regex=True).str.replace("]", "", regex=True).str.replace('"', "")
        df["tag"] = df.summary.str.lower().apply(get_tag, args=(list(idx_tags.keys()),))
        df["project_def_id"] = df.tag.str.lower().replace(idx_tags)
        df["submitter_id"] = user_id
    return df


def get_inner_dict(projects: list):
    new_projects = []
    for p_dict in projects:
        p_dict["project"] = p_dict["project_def"]["project"]["label"]
        p_dict["task"] = p_dict["project_def"]["task"]["label"]
        p_dict["customer"] = p_dict["project_def"]["customer"]["label"]
        p_dict.pop("project_def")
        new_projects.append(p_dict)
    return new_projects


def load_cal_by_sql(user_id: int, year: Optional[int] = None, month: Optional[int] = None) -> Optional[pd.DataFrame]:

    if year and month:
        results = get("calendar", f"bulk/{year}/{month}")
    else:
        results = get("calendar/bulk/all")

    df = pd.DataFrame()
    if len(results) > 1:
        df = pd.DataFrame(get_inner_dict(results))
    return df


def find_errors(df: pd.DataFrame) -> pd.DataFrame:
    errs = df.loc[
        df.tag == "NaN",
        ["summary", "startdate", "enddate"],
    ]
    errs.startdate = errs.startdate.dt.strftime("%d.%m.%Y %H:%M")
    errs.enddate = errs.enddate.dt.strftime("%d.%m.%Y %H:%M")
    return errs


def get_tag(sentence: Optional[str], *args: list) -> str:
    """Get the first matching tag in a sequence of words

    Args:
        sentence (str): A subject sentence.
        allowed_tags (dict): Allowed tags and their synonyms.

    Returns:
        [str]: First matching tag.
    """
    allowed_tags = args[0]  # list(map(lambda x: x.lower(), args[0]))
    if sentence:
        words = sentence.split()
    else:
        words = []
    try:
        tag_of_close_matches = [
            difflib.get_close_matches(word, allowed_tags, n=1, cutoff=0.85) if word.startswith("#") else [None]
            for word in words
        ][0]
    except:
        tag_of_close_matches = [None]

    try:
        first_matching_tag = list(filter(None, tag_of_close_matches))[0]
    except IndexError:
        first_matching_tag = "NaN"

    return first_matching_tag


def flatten(alist: list) -> list:
    return [item for sublist in alist for item in sublist]


def save_dataframe(df: pd.DataFrame):
    json_string = df.to_json(orient="records")
    data = literal_eval(json_string)
    post("calendar/bulk", data)


def fix_dataframe(df: pd.DataFrame, tags: dict) -> pd.DataFrame:
    for tag, indexes in state().fixtures.items():
        for idx in indexes:
            df.loc[idx, "tag"] = tag
            df.loc[idx, "project_def_id"] = tags[tag]
    return df


def app() -> None:
    """Create a startpage"""
    st.title("📆 Kalender API")
    st.markdown(
        """**Achtung** Der Kalender wird nach erstem Laden auf dem Server gespeichert.
        Bei Änderungen im Cloud-Kalender bitte **Reload Kalender** nutzen."""
    )
    s = Session()
    col1, col2, col3 = st.columns(3)
    cal = col1.text_input(label="Cloud Kalendername", value="Personal")
    if col3.button("🔄 Kalender neuladen"):
        LOGGER.warning(delete("calendar", f"bulk/{s.year}/{s.month}"))
        st.experimental_rerun()

    if load_cal_by_sql(s.uid, s.year, s.month).empty:

        tags = {d["label"]: d["project_def_id"] for d in get("tag-all")}

        df = get_calendar_data(
            s.uid,
            s.month,
            s.year,
            cal,
            s.name,
            decrypt_password(s.hashed_password),
            tags,
        )
        if df.empty:
            st.error(f"In der Cloud sind keine Kalendereinträge für {s.year}-{s.month} vorhanden!")
        else:
            errs = find_errors(df)

            # Get stuff to replace in dataframe later
            if state().fixtures:
                flat_fixtures = flatten(list(state().fixtures.values()))
            else:
                flat_fixtures = []

            if len(errs) != len(flat_fixtures) or not errs.empty:
                with st.form("Korrektur"):
                    st.subheader("Korrektur nicht erkannter Kalendereinträge")
                    st.warning("Aktueller Kalender geladen. Es gibt einige fehlerhafte Einträge!")
                    options = [idx for idx in list(errs.index.values) if idx not in flat_fixtures]
                    st.dataframe(errs.loc[options])
                    col1, col2 = st.columns(2)
                    idx = col1.multiselect(
                        label="Welches Projekt soll überarbeitet werden?",
                        options=options,
                    )
                    tag = col2.selectbox(
                        label="Bitte wähle ein Schlüsselwort:",
                        options=list(tags.keys())[1:],
                    )

                    if st.form_submit_button("Korrigieren"):
                        if tag in state().fixtures:
                            if isinstance(idx, list):
                                state().fixtures[tag] + idx
                            else:
                                state().fixtures[tag].append(idx)
                        else:
                            state().fixtures[tag] = idx
                        st.experimental_rerun()
            else:
                st.success("Es wurden alle Tags erkannt!")

            save = False
            _, center, _ = st.columns(3)
            if center.button("❌ Einträge verwerfen"):
                save = True
                df = df.drop(options)

            if len(errs) == len(flat_fixtures) or save:
                save_dataframe(fix_dataframe(df, tags))
                st.spinner("Speichern")
                st.experimental_rerun()

    else:
        st.success("Der Kalendareintrag existiert bereits!")
        # reload_state = st.button("Kalender neu laden")
        # if reload_state:  # or df.empty:
        #     LOGGER.warning(delete("calendar", f"bulk/{s.year}/{s.month}"))
        #     st.experimental_rerun()

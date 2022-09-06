import streamlit as st
import pandas as pd
from ast import literal_eval
from app.core.auth import Session, state, decrypt_password
from app.core.api import get, post
from app.pages2.calendar import MyCalendar
from datetime import time, timedelta, datetime


def filter_name(data: dict, literal: str = "NaN") -> str:
    return data["label"] if data["label"] != literal else ""


# @st.cache()
def get_day(year: int, month: int, day: int):
    return get(f"calendar/bulk/{year}/{month}/{day}")


# @st.cache()
def get_tags() -> tuple:
    # TODO Userabhängige Hashtags
    all_tags = get("tag-all")
    tags = {d["label"]: d["project_def_id"] for d in all_tags}
    idx_tags = {k.lower(): v for k, v in tags.items()}
    return tags, idx_tags


# @st.cache()
def format_calendar(data: list, idx_tags: list, uid: int) -> pd.DataFrame:
    df = pd.DataFrame(data, columns=["Start", "Ende", "Tag", "Datum"])
    df["startdate"] = df.apply(lambda r: pd.datetime.combine(r["Datum"], r["Start"]), 1)
    df["enddate"] = df.apply(lambda r: pd.datetime.combine(r["Datum"], r["Ende"]), 1)
    df["summary"] = df.Tag
    df["duration"] = (df.enddate - df.startdate).astype("timedelta64[m]") / 60
    df["submitter_id"] = uid
    df["project_def_id"] = df.Tag.str.lower().replace(idx_tags)
    return df[df.columns[4:]]


def save_df_to_db(df: pd.DataFrame) -> None:
    json_string = df.to_json(orient="records")
    data = literal_eval(json_string)
    post("calendar/bulk", data)


def app() -> None:
    st.title("⏰ Arbeitszeitplanung")
    s = Session()
    tags, idx_tags = get_tags()
    c1, _, _, _ = st.columns(4)
    if not len(state().times):
        start = time(8, 0)
        end = time(9, 0)
        date = datetime.now().date()
    else:
        start, end, _, date = state().times[-1]
        start = end
        end = time(end.hour + 1, 0)
        df = pd.DataFrame([l[:3] for l in state().times], columns=["Start", "Ende", "Tag"])
        df.Start, df.Ende = df.Start.astype(str), df.Ende.astype(str)
        st.write(df)

    # TODO Check if date exists in database
    date = c1.date_input(
        "Datum",
        value=date,
    )
    r = get_day(date.year, date.month, date.day)
    if "detail" in r:
        with st.form("Timeslider"):

            start, end = st.slider(
                "Arbeitszeit",
                value=(start, end),
                step=timedelta(minutes=15),
                min_value=time(6, 0),
                max_value=time(21, 0),
            )

            tag = st.selectbox("Hashtag", tags)

            if st.form_submit_button("Hinzufügen"):
                data = (start, end, tag, date)
                if len(state().times) == 0:
                    state().times = [data]
                else:
                    state().times.append(data)
                st.experimental_rerun()

        _, c2, c3, c4 = st.columns(4)
        if c2.button("Save day"):
            df = format_calendar(data=state().times, idx_tags=idx_tags, uid=s.uid)
            save_df_to_db(df)
            st.success("In Datenbank gespeichert!")
            st.experimental_rerun()

        if c3.button("Sync Cloud"):
            try:
                df = format_calendar(data=state().times, idx_tags=idx_tags, uid=s.uid)
                cal_name = "personal"
                base_url = f"https://cloud.amitronics.net/remote.php/dav/calendars/{s.name}/{cal_name}/"
                cal = MyCalendar(base_url)
                cal.connect_server(s.name, decrypt_password(s.hashed_password))
                cal.get_calendar(cal_name.lower())
                for _, row in df.iterrows():
                    cal.create_event(start=row["startdate"], end=row["enddate"], summary=row["summary"])
                st.success("Mit Cloud Kalender synchronisiert!")
            except:
                st.error("Not correctly implemented yet!")

        if c4.button("Alle Löschen"):
            state().times = []
            st.experimental_rerun()
    else:
        st.success("Der Arbeitstag existiert bereits in der Datenbank!")
        df = pd.DataFrame(r)
        df["Start"] = pd.to_datetime(df["startdate"]).dt.time.astype(str)
        df["Ende"] = pd.to_datetime(df["enddate"]).dt.time.astype(str)
        df["Tag"] = df.summary
        st.write(df[["Start", "Ende", "Tag"]])

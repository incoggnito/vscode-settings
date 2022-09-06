import streamlit as st
import re
import time
import pandas as pd
from datetime import date, timedelta, datetime
from restapi import AnueTimesheet, KimaiAPI
from app.core.auth import Session

LOGGER = logging.getLogger(__name__)


# api = KimaiAPI()
# # TODO Read excel or pdf

# pdf_text = f.read()
# data = pdftext2json(pdf_text, 3, 2022, 7)
# df = pd.DataFrame(data)
# timesheets = [AnueTimesheet(d) for d in data]

def pdftext2json(pdf_text: str, user: int, year: int, month: int) -> dict:
    results = list()
    for line in pdf_text.split("\n"):
        d = dict()
        if re.match(r"\d{2}\s[M|T|W|F]*", line):
            words = line.split()
            day = int(words[0])
            if re.match(r"\d{2}:\d{2}", words[2]):
                start_time = words[2]
                if re.match(r"\d{2}:\d{2}", words[3]):
                    end_time = words[3]
                    activity = [473, 297]
            elif re.match(r"^Schichttausch\s", words[2]):
                activity = [8, 160]
                start_time = "00:00"
                end_time = "23:59"
            else:
                LOGGER.warning("Can't parse the text information")

            try:
                s = start_time.split(":")
                e = end_time.split(":")
                d["begin"] = datetime(year, month, day, int(s[0]), int(s[1]))
                d["end"] = datetime(year, month, day, int(e[0]), int(e[1]))
                d["project"] = activity[0]
                d["activity"] = activity[1]
                d["user"] = user
                results.append(d)
            except:
                LOGGER.warning("No valid kimai entry!")
    return results

def app() -> None:
    """Run projecthours page"""

    st.title("🤮 Abwesenheit")
    s = Session()

    special_days = {
        "🏖 Urlaub": 12,
        "🤮 Krankheit": 13,
        "🚵‍♂️ Gleittag": 14,
        "👩‍🎓 Weiterbildung": 15,
        "🍺 Sonderurlaub": 16,
    }
    options = ("Neue Anfrage", "Bearbeiten", "Löschen")

    # TODO: get data from (pending) vacation endpoint
    # some dummy data ...
    format_str = "%d.%m.%Y"
    vac_begin = date.today().strftime(format_str)
    vac_end = date.today() + timedelta(days=7)
    vac_end = vac_end.strftime(format_str)
    sick = date.today() + timedelta(days=-10)
    sick = sick.strftime(format_str)
    data = {
        "ID": [1, 2],
        "Typ": ["Urlaub", "Krankheit"],
        "Beginn": [vac_begin, sick],
        "Ende": [vac_end, sick],
        "Status": ["noch nicht angenommen", "akzeptiert"],
    }
    df = pd.DataFrame(data)
    st.write("Übersicht")
    st.dataframe(df)
    option_col, _, _ = st.columns([1, 2, 2])

    with option_col:
        option = st.selectbox("Wähle dein Anliegen", options)

    if option == "Neue Anfrage":
        with st.form("Neue Anfrage"):
            event = st.selectbox("Wähle", special_days.keys())
            if event:
                col1, col2 = st.columns(2)
                with col1:
                    start = st.date_input("Beginn")
                with col2:
                    end = st.date_input("Ende")
                comment = st.text_area(
                    "Kommentar", placeholder="Hier kannst du deinem Teamleiter eine Nachricht mitgeben."
                )
                if st.form_submit_button("Anfrage abschicken"):
                    # TODO:
                    # get uid / email from team lead
                    # send email to team lead
                    with st.spinner("senden ..."):
                        time.sleep(1)
                    st.success(f"Anfrage für {event} versendet!\nDein Teamleiter wurde per E-Mail informiert.")

    elif option == "Bearbeiten":

        with st.form("Bearbeiten"):
            event_idx = [1, 2]  # TODO get mutable events from endpoint
            event_id = st.selectbox("Bitte ID auswählen", event_idx)
            if event_id:
                # TODO:
                # load data from endpoint and display
                col1, col2 = st.columns(2)
                with col1:
                    start = st.date_input("Beginn")
                with col2:
                    end = st.date_input("Ende")
                comment = st.text_area(
                    "Kommentar", placeholder="Hier kannst du deinem Teamleiter eine Nachricht mitgeben."
                )
                if st.form_submit_button("Anfrage bearbeiten"):
                    # TODO:
                    # get uid / email from team lead
                    # send email to team lead
                    with st.spinner("senden ..."):
                        time.sleep(1)
                    st.success(
                        f"Eintrag mit der ID {event_id} erfolgreich bearbeitet!\nDein Teamleiter wurde per E-Mail informiert."
                    )

    elif option == "Löschen":

        event_idx = [1, 2]  # TODO get deletable events from endpoint
        event_id = st.selectbox("Bitte ID auswählen", event_idx)

        with st.form("Löschen"):

            if event_id:
                comment = st.text_area(
                    "Kommentar", placeholder="Hier kannst du deinem Teamleiter eine Nachricht mitgeben."
                )
                st.warning(f"Eintrag mit der ID {event_id} jetzt löschen?")
                if st.form_submit_button("Löschen"):
                    with st.spinner("löschen ..."):
                        time.sleep(1)
                    st.success(
                        f"Eintrag mit der ID {event_id} erfolgreich gelöscht!\nDein Teamleiter wurde per E-Mail informiert."
                    )
    else:
        pass

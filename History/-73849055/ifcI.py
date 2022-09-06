import streamlit as st
import time
import pandas as pd
from datetime import date, timedelta

from app.core.auth import Session


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

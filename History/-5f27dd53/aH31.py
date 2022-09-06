# """Main application for Time Management"""
import logging
import streamlit as st
from app.utils.multipage import MultiPage
from app.core import auth
from app.core import config

from app.pages import (
    absence,
    calendar,
    hours,
    projecthours,
    workinghours,
    contract,
    admin
)
from app.page.sidebar import add_sidebar

LOGGER = logging.getLogger(__file__)

st.set_page_config(layout="wide")

if not auth.state().token:
    auth.uid_from_token()

if auth.state().token:

    add_sidebar()

    if auth.state().user["pw_last_set"]:
        app = MultiPage()

        # user section
        if "AMI" in auth.state().user["groups"]:
<<<<<<< HEAD
            app.add_page("📆 Kalender API", calendar.app)
            app.add_page("🕚 Stundenabrechnung", workinghours.app)

        # team lead section
        if "TL" in auth.state().user["groups"] or "GF" in auth.state().user["groups"]:
            app.add_page("Monatliche Abrechnung", budget.app)
=======
            # app.add_page("⏰ Arbeitszeiterfassung", timeshift.app)
            app.add_page("📆 Kalender API", calendar.app)
            app.add_page("🕚 Stundenabrechnung", workinghours.app)
            app.add_page("📈 Projektstunden", projecthours.app)
            app.add_page("🤮 Abwesenheit", absence.app)

        # team lead section
        if "TL" in auth.state().user["groups"] or "GF" in auth.state().user["groups"]:
            # app.add_page("🏷️ Projektverwaltung", tags.app)
            # app.add_page("📊 Projektstatistik", statistic.app)
            pass
>>>>>>> 2a98e94639a8c30d501f874e5ce9e0181ff19565

        # human resources and server admin section
        if "HR" in auth.state().user["groups"] or "ServerAdmin" in auth.state().user["groups"]:
            app.add_page("🤼 Stundenübersicht", hours.app)
            app.add_page("📇 Arbeitsverträge", contract.app)
            app.add_page("🧾 Rechnungsablage", invoices.app)
        app.run()
    else:
        LOGGER.warning(f"Not authenticated")

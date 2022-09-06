# """Main application for Time Management"""
import logging
import streamlit as st

# from app.utils.multipage import MultiPage
from streamlit_multipage import MultiPage
from app.core import auth
from app.core import config

from app.pages import (
    calendar,
    hours,
    projecthours,
    statistic,
    tags,
    workinghours,
    contract,
    timeshift,
    admin,
)
from app.pages.sidebar import add_sidebar

# from viztracer import VizTracer

app = MultiPage()
app.st = st

LOGGER = logging.getLogger(__file__)

if not auth.state().token:
    auth.uid_from_token()

if auth.state().token:

    # Profile the code
    # with VizTracer(output_file="profile.json"):
    # add_sidebar()

    # if auth.state().user["pw_last_set"]:
    #     app = MultiPage()
    #     app.add_page("⏰ Arbeitszeiterfassung", timeshift.app)
    #     app.add_page("🏷️ Projektverwaltung", tags.app)
    #     app.add_page("📆 Kalender API", calendar.app)
    #     app.add_page("🕚 Stundenabrechnung", workinghours.app)
    #     app.add_page("📈 Projektstunden", projecthours.app)
    #     if auth.state().user["groups"] == "TL" or auth.state().user["groups"] == "GF":
    #         app.add_page("📊 Projektstatistik", statistic.app)
    #         # if auth.state().user["groups"] == "HR": # TODO Enable HR Role
    #         app.add_page("🤼 Stundenübersicht", hours.app)
    #         app.add_page("📇 Arbeitsverträge", contract.app)
    #         app.add_page("👑 Administration", admin.app)
    #     app.run()
    # else:
    #     LOGGER.warning(f"Not authenticated")

app.start_button = "Go to the main page"
app.navbar_name = "Other Pages:"
app.next_page_button = "Next Chapter"
app.previous_page_button = "Previous Chapter"
app.reset_button = "Delete Cache"
app.navbar_style = "SelectBox"

app.header = header
app.footer = footer
app.navbar_extra = sidebar

app.hide_menu = True
app.hide_navigation = True

app.add_app("Landing", landing_page, initial_page=True)
app.add_app("Input Page", input_page)
app.add_app("BMI Result", compute_page)

app.run()
# """Main application for Time Management"""
import logging
import streamlit as st

# from app.utils.multipage import MultiPage
from streamlit_multipage import MultiPage
from app.core import auth

# from app.core import config


def footer(st):
    st.write("Created by [a.hofer & m.kessler](https://elc.github.io)")


def header(st):
    st.write("This app is free to use")


# from app.pages import (
#     calendar,
#     hours,
#     projecthours,
#     statistic,
#     tags,
#     workinghours,
#     contract,
#     timeshift,
#     admin,
# )
from app.pages import timeshift
from app.pages.sidebar import sidebar

# from viztracer import VizTracer

st.set_page_config(
    page_title="Projektstunden",
    page_icon="🕚",
    layout="wide",
)

app = MultiPage()
app.st = st

LOGGER = logging.getLogger(__file__)

if not auth.state().token:
    auth.uid_from_token(st)

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

    app.add_app("⏰ Arbeitszeiterfassung", timeshift.app, initial_page=True)
    # app.add_app("🏷️ Projektverwaltung", tags.app)
    # app.add_app("📆 Kalender API", calendar.app)

    app.run()
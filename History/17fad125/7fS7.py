# """Main application for Time Management"""
import logging
from app.utils.multipage import MultiPage
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

from viztracer import VizTracer

LOGGER = logging.getLogger(__file__)

@profile
def main ():
    if not auth.state().token:
        auth.uid_from_token()

    if auth.state().token:

        # Profile the code
        with VizTracer(output_file="profile.json"):
            add_sidebar()

            if auth.state().user["pw_last_set"]:
                app = MultiPage()
                app.add_page("⏰ Arbeitszeiterfassung", timeshift.app)
                app.add_page("🏷️ Projektverwaltung", tags.app)
                app.add_page("📆 Kalender API", calendar.app)
                app.add_page("🕚 Stundenabrechnung", workinghours.app)
                app.add_page("📈 Projektstunden", projecthours.app)
                if auth.state().user["groups"] == "TL" or auth.state().user["groups"] == "GF":
                    app.add_page("📊 Projektstatistik", statistic.app)
                if auth.state().user["groups"] == "ServerAdmin": # TODO Enable HR Role
                    app.add_page("🤼 Stundenübersicht", hours.app)
                    app.add_page("📇 Arbeitsverträge", contract.app)
                    app.add_page("👑 Administration", admin.app)
                app.run()
            else:
                LOGGER.warning(f"Not authenticated")

if __name__ == "__main__":
    main()
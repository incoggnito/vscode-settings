# Testing
import os
import logging

from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

if os.getenv("API_LOGIN_URL"):
    logger.info("Load environment variables from docker!")
else:
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    if os.getenv("API_LOGIN_URL"):
        logger.info("Load env variables from .env file!")
    else:
        logging.error("Can't find the env variables!")
        raise EnvironmentError


LOGIN_URL = os.getenv("API_LOGIN_URL")
LOGOUT_URL = os.getenv("AUTHENTIK_LOGOUT_URL")
API_URL = os.getenv("API_URL")
SECRET = os.getenv("JWT_SECRET").encode("utf-8")

USER_ENDPOINT = f"{API_URL}user/"
META_ENDPOINT = f"{API_URL}meta/"

# --------------------------------------------------------------------

G_GF = "GF"
G_BRAKE = "BRAKE"
G_SIM = "SIM"
G_TL = "TL"
G_ADMIN = "ServerAdmin"
G_ANUE = "ANUE"
G_USER = "USER"

# ----------------------------------------------------------------
PAUSE = ["Pause", "Mittag"]
SPECIAL_PROJECTS = {
    "U": 12,
    "K": 13,
    "G": 14,
    "W": 15,
    "S": 16,
}

SPECIAL_Tags = {
    "U": "Urlaub",
    "K": "Krankheit",
    "G": "Gleittag",
    "W": "Weiterbildung",
    "S": "Sonderurlaub",
    "F": "Feiertag",
}

VIEW = [
    "KW",
    "Wochentag",
    "Abwesenheit",
    "Arbeitsbeginn",
    "Arbeitsende",
    "Pause",
    "Arbeitszeit",
    "Zusatzpause",
    "Überstunden",
]

DAY_ABBR = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

LAW = """**Gesetzliche Ruhepausen gemäß § 4 ArbZG**   
- von 6 - 9 Arbeitsstunden = 30 min Pause 
- ab        9 Arbeitsstunden = 45 min Pause

Die gesetzl. Pausen werden in der Berechnung der Arbeitszeit automatisch abgezogen!
Bitte beachtet auch die max. Arbeitszeit von 10 Stunden/Tag!"""

LAW_ANUE_BMW = """Ruhepausen in der ANÜ bei BMW:   
- unter 4,5 Arbeitsstunden = 00 min Pause 
- ab 4,5 bis 6 Arbeitsstunden = 15 min Pause
- ab 6 Arbeitsstunden = 60 min Pause	

Die Pausen werden in der Berechnung der Arbeitszeit automatisch abgezogen!
Bitte beachtet auch die max. Arbeitszeit von 10 Stunden/Tag!"""

# TOKEN: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ijc3NWY5ZTdlMzA5NGExZGFhNTZmOWJhYmU4MTY4N2I2In0.eyJpc3MiOiJodHRwczovL2FtaXRyb25pY3MubmV0L2FwcGxpY2F0aW9uL28vcGgvIiwic3ViIjoiZDEwNTNhZDRhNjQyMzAwYzEzZjcyMmQ2MWY0ZTA0NmY2NzMzNGNlZThhOTg3ZDQ1ZjZlNWI4YjhmZGI0ZTVmOSIsImF1ZCI6Ijk2MWFmM2FkZjkyY2Q1N2RiMzE4ZWQ2YTM3NTEyMTBjYTFhNTJhMmEiLCJleHAiOjE2NDU5ODIwMTYsImlhdCI6MTY0MzM5MDAxNiwiYXV0aF90aW1lIjoxNjQzMzg3MDIwLCJhY3IiOiJnb2F1dGhlbnRpay5pby9wcm92aWRlcnMvb2F1dGgyL2RlZmF1bHQiLCJjX2hhc2giOm51bGwsIm5vbmNlIjoiVVI3ekk4cUxKdlZKclVRT1lKM2MiLCJhdF9oYXNoIjoiSllyNTNBdVpOckZLdDNkem13U2ZXUSIsIm5hbWUiOiJBbmRyZWFzIEhvZmVyIiwiZ2l2ZW5fbmFtZSI6IkFuZHJlYXMgSG9mZXIiLCJmYW1pbHlfbmFtZSI6IiIsInByZWZlcnJlZF91c2VybmFtZSI6ImEuaG9mZXIiLCJuaWNrbmFtZSI6ImEuaG9mZXIiLCJ1aWQiOiIzOCIsImdyb3VwcyI6WyJTZXJ2ZXJBZG1pbiIsIkNvb3BlcmF0aW9uIiwiRm9yc2NodW5nIiwiVW16dWciLCJCUkFLRSIsIkdJVCIsIkJNVyIsIkFNSSIsIlRMIiwiRkUtQnVjaGhhbHR1bmciXX0.GflxLfJ57HzN6MA0JAJgdix8KPnA5O391beJy1EQEc6pTfIGl6iIc09zO9Y1Ca5XIslN-HzJpyq5tkz7qRHHXWiup9DY7k9cIUtrMIBP2V6fYKfvRVOYrcE-G_Nsar5YoMm0N6177B5KWfuoYXWr_xeA7uKorTeOyji5Jk6dXBaBeKP79tgxfLZgrSqTJ5_e2vp7cSDOoVGVxdvmvCACEPOApQO4w8J7qAN_hCc8tfp7cHeYLgg-gnawa1lMtD9gRCLCYXe6ucKabUPqS1dUnocnUJmftCKV4F5koDeiys7k7kid2J4mZkO6Q9y_0A6haAZJpKmonyW7q6eWJ7OWpXfuOVVmI5J03gfYU_Rbm0VQi3RP9GmBUgBKAkMH8ajj2MYSpnsnDudMfV2d0heVcqVubGrUbV4JwxqvMvFkDZ10o7Tsp51-oPj5XU4CLDqwSqMYZJYVAWpIkmZ_1nDQOAehs6x62cOQ36VXLeP3bjWTKJsgfEn98cUqwh3T1rJ-AL8Yk2Yt4UDDvxQ99Cw1usUwb3f-YxinjfRfAJhUtq3Nphs6f-QroixUveD0C5ODRVuIf8d_-UADuIC1RMR_feFpal-R7Mf1Cwlu2F3aAhE5OIkHsTDPxzby5_QqRojEUXF9qaJc91vKMixKm4AMoACfnLPKov8QeKQ8dhQStbI"
# USERMETA: dict = {
#     "id": 1,
#     # "uid": 38,
#     "is_superuser": True,
#     "workdays": 5,
#     "workhours": 8,
#     "province": "BY",
#     "vacation": 30,
#     "pw_last_change": None,
# }

# PROJECTS: dict = {
#     "submitter_id": 38,
#     "customer": "Antares",
#     "project": "Laserschutz",
#     "task": "Untersuchung",
#     "description": "",
#     "group": "Auftrag",
# }

# TAGS: dict = {"project_def_id": 1, "submitter_id": 38, "tag": "Antares"}
import time
import logging

# import requests
from streamlit_multipage import MultiPage
from app.pages.calendar import get_month, get_year
from PIL import Image
from app.core.auth import state, encrypt_password, read_user_monthly, read_user_meta
from app.core.api import get, put
from app.core import config

LOGGER = logging.getLogger(__name__)


def set_new_password():
    state().user["pw_last_set"] = None


def get_major_group(groups: list):
    if config.G_ADMIN in groups:
        return config.G_ADMIN
    elif config.G_GF in groups:
        return config.G_GF
    elif config.G_TL in groups:
        return config.G_TL
    elif config.G_BRAKE in groups:
        return config.G_BRAKE
    elif config.G_SIM in groups:
        return config.G_SIM
    elif config.G_ANUE in groups:
        return config.G_ANUE
    else:
        return config.G_USER


# @st.cache()
def load_meta(year: int, month: int) -> dict:
    return read_user_meta(year, month)


# @st.cache()
def load_monthly(year: int, month: int) -> dict:
    return read_user_monthly(year, month)


def sidebar(st, **state) -> None:
    @st.cache
    def load_logo() -> Image:
        image = Image.open("data/img/logo.png")
        return image

    def set_auth_message(msg, type="info", delay=0.5, show_msgs=True):
        global auth_message
        if type == "warning":
            auth_message = st.warning
        elif type == "success":
            auth_message = st.success
        elif type == "error":
            auth_message = st.error
        else:  # default type == const.INFO:
            auth_message = st.info
        if show_msgs:
            auth_message(msg)
            if delay:
                time.sleep(delay)
                auth_message = st.empty()

    """Add stuff to the sidebar"""
    st.sidebar.image(load_logo())

    # uid = state().payload["uid"]
    if not "user" in state:
        MultiPage.save({"user": get("user")})

    if st.sidebar.button("Passwort zurücksetzen"):
        LOGGER.info("password reset button pressed")
        set_new_password()

    # Update user data
    if not state.user["pw_last_set"]:
        set_auth_message("Bitte Cloud mit App-Passwort registrieren!", delay=None, show_msgs=True)
        with st.sidebar.form("login_form"):

            name = st.text_input("Username:")
            pw = st.text_input("Passwort eingeben", type="password")

            if st.form_submit_button(label="Speichern"):
                data = {"name": name, "hashed_password": encrypt_password(pw)}
                response = put("user", data)
                st.experimental_rerun()

    else:
        month = st.sidebar.number_input(label="Month", value=get_month(), min_value=1, max_value=12)
        year = st.sidebar.number_input(label="Year", value=get_year(), min_value=2021, max_value=None)

        d = load_meta(year, month)
        meta_year, meta_month = d["meta_year"], d["meta_month"]
        meta = {"groups": get_major_group(state.payload["groups"])}
        state.user["groups"] = meta["groups"]
        put("meta", query=f"{meta_year}/{meta_month}", data=meta)
        load_monthly(year, month)
        state.cal = {"year": year, "month": month}
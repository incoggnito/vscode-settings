import streamlit as st
from cryptography.fernet import Fernet
import logging
import jwt
from app.core import config
from app.core.api import get

LOGGER = logging.getLogger(__file__)


def unpack_token(id_token: str) -> dict:
    decoded_token = jwt.decode(id_token, options={"verify_signature": False})  # TODO Add signature
    return {k: v for k, v in decoded_token.items() if k == "uid" or k == "groups"}


# class Session:
#     uid: int
#     groups: str
#     id: int
#     date_created: str
#     workhours: int
#     workdays: int
#     province: str
#     vacation: float
#     submitter_id: int
#     name: str
#     email: str
#     is_superuser: bool
#     hashed_password: str
#     pw_last_set: str
#     month: int
#     year: int
#     flextime: float
#     last_month_vacation: float
#     last_valid_month: int
#     last_valid_year: int
#     meta_year: int
#     meta_month: int
#     rest_vacation_last_year: float

#     def __init__(self):
#         entries = {}
#         entries.update(state().payload)
#         entries.update(state().user)
#         entries.update(state().cal)
#         if state().monthly:
#             entries.update(state().monthly)
#         self.__dict__.update(entries)


# def state():
#     if "token" not in st.session_state:
#         st.session_state.token = None
#     if "user" not in st.session_state:
#         st.session_state.user = None
#     if "payload" not in st.session_state:
#         st.session_state.payload = None
#     if "fixtures" not in st.session_state:
#         st.session_state.fixtures = {}
#     if "cal" not in st.session_state:
#         st.session_state.cal = {}
#     if "monthly" not in st.session_state:
#         st.session_state.monthly = None
#     if "times" not in st.session_state:
#         st.session_state.times = []
#     return st.session_state


def uid_from_token() -> None:
    """Retrieve the token from authentik redirect url

    Returns:
        bool: User is authenticated
    """
    # TODO Change this later
    params = st.experimental_get_query_params()
    # params = {"id_token": [config.TOKEN]}

    if not ("id_token" in params):
        st.warning("You are not authenticated. Please follow this link:")
        link = f'<a href="{config.LOGIN_URL}" target="_self">Login</a>'
        st.markdown(link, unsafe_allow_html=True)
    else:
        state().token = params["id_token"][0]
        data = unpack_token(state().token)
        state().payload = data
        st.experimental_set_query_params()


def encrypt_password(pw: str) -> str:
    pw = pw.encode("utf-8")
    cipher_suite = Fernet(config.SECRET)
    return cipher_suite.encrypt(pw).decode("utf-8")


def decrypt_password(hashed_pw: str) -> str:
    hashed_pw = hashed_pw.encode("utf-8")
    cipher_suite = Fernet(config.SECRET)
    return cipher_suite.decrypt(hashed_pw).decode("utf-8")


def read_user_meta(year: int, month: int) -> dict:
    """Get the contract information.

    Args:
        id (int): Primary User Key
    """

    d = get(f"meta/{year}/{month}")
    d["meta_year"], d["meta_month"] = d["year"], d["month"]
    d.update(d["submitter"])
    d.pop("submitter")
    state().user = d
    return d


def read_user_monthly(year: int, month: int) -> None:
    """Get the contract information.

    Args:
        id (int): Primary User Key
    """
    lastmonth = month - 1
    year_turn = False
    # check year turn
    if lastmonth == 0:
        year_turn = True
        year = year - 1
        lastmonth = 12

    # get rest vacation last year
    if year_turn:
        r = get(f"monthly/{year}/{12}")
    else:
        r = get(f"monthly/{year -1 }/{12}")
    rest_vacation_last_year = r["vacation"]

    # get monthly carry from last month
    r = get(f"monthly/{year}/{lastmonth}")
    if not "detail" in r:
        try:
            if year_turn:
                r["last_month_vacation"] = state().user["vacation"] + r["vacation"]
            else:
                r["last_month_vacation"] = r["vacation"]
            r["rest_vacation_last_year"] = rest_vacation_last_year
            r["last_month"], r["last_year"] = r["month"], r["year"]
            for item in ["vacation", "month", "year"]:
                r.pop(item)
            state().monthly = r
        except KeyError as e:
            LOGGER.error(f"A KeyError occurred: {e}")
    else:
        state().monthly = None

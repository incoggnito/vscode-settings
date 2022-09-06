import streamlit as st
from app.core.api import delete, get
from app.pages2.calendar import get_year, get_month


def app() -> None:
    """Run projecthours page"""
    st.title("👑 Administration")
    users = {user["name"]: user["uid"] for user in get("user/all")}
    with st.form("Select"):
        st.subheader("Mitarbeiter Monatskorrektur")
        st.write(
            "Löschung des Übertrags aus der Stundenabrechnung und damit Freigabe zur Neubefüllung durch den Mitarbeiter."
        )
        user = st.selectbox("Mitarbeiter", users.keys())
        uid = users[user]
        month = st.number_input(label="Month", value=get_month(), min_value=1, max_value=12)
        year = st.number_input(label="Year", value=get_year(), min_value=2021, max_value=None)

        if st.form_submit_button("Löschen"):
            r = delete(f"monthly/{year}/{month}/{uid}")
            if "deatail" in r:
                st.error(r["detail"])
            else:
                st.success(f"Erfolgreiche Löschung des Monatsübertrags am {month}-{year} für {user}!")

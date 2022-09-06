import streamlit as st
import pandas as pd
from app.core.api import get, put, post
from app.pages.calendar import get_year, get_month


def update_user_attr(meta: list):
    new_meta = []
    for p_dict in meta:
        p_dict["name"] = p_dict["submitter"]["name"]
        p_dict["uid"] = p_dict["submitter"]["uid"]
        p_dict.pop("submitter")
        new_meta.append(p_dict)
    return new_meta


cols = {
    "name": "Name",
    "uid": "Personalnr.",
    "date_created": "Datum",
    "workdays": "Arbeitstage",
    "workhours": "Arbeitsstunden",
    "province": "Bundesland",
    "vacation": "Urlaub",
}


def app() -> None:

    st.title("📇 Arbeitsverträge")
    st.markdown("""Hier können Änderungen im Arbeitsvertrag verzeichnet werden.""")
    # TODO Update if value changed
    df = pd.DataFrame(update_user_attr(get("meta/all")))
    if not df.empty:
        df.groupby("uid").last()
        view = df.loc[:, cols.keys()]
        view.columns = cols.values()
        view = view.convert_dtypes()
        view.Datum = pd.to_datetime(view.Datum).dt.date
        view.set_index("Personalnr.", inplace=True)
        view = view.sort_index()
        styler = view.style.format(subset=["Arbeitsstunden"], decimal=",", precision=1).bar(
            subset=["Arbeitsstunden"], align="mid"
        )
        st.write(styler)

        with st.form("EditMeta"):
            action = st.selectbox("Aktion", ["Neuer Eintrag", "Korrektur"])
            uid = st.number_input("Personalnummer", min_value=1, step=1, max_value=100)
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            workdays = col1.number_input("Wochentage", min_value=1, max_value=5, value=5)
            workhours = col2.number_input("Wochenstunden", min_value=1, max_value=50, value=40)
            vacation = col3.number_input("Urlaubsanspruch", min_value=1, max_value=50, value=30)
            province = col4.selectbox("Bundesland", ["BY", "SN"], key="BY")
            year = col5.number_input("Vertragsjahr", value=get_year(), min_value=2021, step=1)
            month = col6.number_input("Vertragsmonat", value=get_month(), min_value=1, max_value=12)
            data = {
                "workhours": workhours,
                "workdays": workdays,
                "province": province,
                "vacation": vacation,
            }

            if st.form_submit_button("Speichern"):
                if action == "Korrektur":
                    put(f"meta/{year}/{month}/{uid}", data=data)
                else:
                    data["year"], data["month"] = year, month
                    post(f"meta/{uid}", data=data)
    else:
        st.info("Kann keine Daten laden. Fehlende Rechte?")
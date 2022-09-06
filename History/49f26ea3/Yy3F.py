from datetime import datetime
from typing import Optional
import logging
from numpy import empty
import pandas as pd
import numpy as np
import altair as alt

import streamlit as st
from streamlit_tags import st_tags
from app.core.auth import Session
from app.core.api import get, post

import requests

logger = logging.getLogger(__file__)


def filter_name(data: dict, literal: str = "NaN") -> str:
    return data["label"] if data["label"] != literal else ""


# from projecthours.pages.utils import load_tags, save_tags
def edit_field(
    name: str,
    endpoint: str,
    maxtags: int = 1,
    defaults: Optional[list] = None,
    filt: Optional[str] = None,
) -> Optional[tuple]:
    """Load an Index Table,
    edit some changes and return the functions for later creation.

    Args:
        name (str): Display Name
        default (str): Preselection
        endpoint (str): Api endpoint

    Returns:
        tuple: Function and Input Arguments
    """
    data = get(endpoint, filt)
    suggestions = [element["label"] for element in data]

    if not defaults:
        defaults = suggestions

    results = st_tags(
        label=name,
        text="Use TAB, send by ENTER",
        value=defaults,
        suggestions=suggestions,
        maxtags=maxtags,
    )

    if not results:
        results = ["NaN"]

    return (endpoint, results)


# TODO Replace with correct way to access the REST API
# TODO put the response in the correct format for the List
def requestKostenstellen() -> dict:
    headers = {
        "accept": "application/json",
        "X-AUTH-TOKEN": "",
    }
    response = requests.get("https://kimai.amitronics.net/api/activities", headers=headers)
    # print(response.json())
    return response.keys()


def app():
    s = Session()

    st.title("🧾 Leistungskatalog")
    c1, _ = st.columns(2)

    # TODO Correct Database in DF to be set here
    database_df = pd.DataFrame()

    # if projectdef:
    #     st.table(database_df.loc[projectdef])
    projectdef = c1.selectbox(
        "Kostenstelle",
        # TODO REST to get Kostenstellen and then adjust the options to those
        options=("Kostenstelle 1", "Kostenstelle 2", "Kostenstelle 3"),
    )

    with st.form(f"frm"):
        count_col, service_col = st.columns(2)
        (object_col,) = st.columns(1)

        api_calls = []

        # TODO The .split("_") were used in the old format but have
        # to be adjusted to the output of the REST request
        # customer field

        # project field
        with service_col:
            projectdef = c1.selectbox(
                "Leistung",
                # TODO REST to get Leistungen from Activities
                options=("Leistung 1", "Leistung 2", "Leistung 3"),
            )
            # TODO api_calls have to be appended after the database is setup
            # api_calls.append(
            #     edit_field(
            #         name="Artikel",
            #         defaults=product,
            #         endpoint="product",
            #     )
            # )

        # task field
        with count_col:
            cost = st.number_input("Anzahl", min_value=0, max_value=None, value=0)
            # api_calls.append(
            #     edit_field(
            #         name="Kosten",
            #         defaults=cost,
            #         endpoint="cost",
            #     )
            # )

        # startdate field
        with object_col:
            data = st.file_uploader("CSV hochladen")
            # api_calls.append(
            #     edit_field(
            #         name="Datei",
            #         defaults=data,
            #         endpoint="data",
            #     )
            # )

        if st.form_submit_button("Hinzufügen"):
            request_results = {}
            default_name = ""
            for endpoint, data in api_calls:
                submit_data = {"label": data[0] if data[0] else "NaN"}
                response = post(endpoint=endpoint, data=submit_data)
                request_results[f"{endpoint}_id"] = response["id"]
                if not response["label"] == "NaN":
                    default_name = default_name + response["label"] + "_"

            # additional_data = {
            #     "start": str(billdate),
            #     "cost": cost,
            # }
            # request_results = {**request_results, **additional_data}
            request_results = {**request_results}
            pjd_response = post(endpoint="projectdef", data=request_results)

            if len(pjd_response) > 0:
                st.success("Rechnung erfolgreich angelegt / bearbeitet!")
            else:
                st.error("Rechnung konnte nicht angelegt werden")

            st.experimental_rerun()

    # TODO Tabelle mit den Daten aus der Datenbank hinzufügen
    df = pd.DataFrame(np.random.randn(200, 3), columns=["a", "b", "c"])

    c = alt.Chart(df).mark_circle().encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])

    st.altair_chart(c, use_container_width=True)

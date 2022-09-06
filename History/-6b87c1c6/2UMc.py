from typing import Optional
import logging

import streamlit as st
from streamlit_tags import st_tags
from app.core.auth import Session
from app.core.api import get, post

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


def app():
    s = Session()

    st.title("🏷️ Projektverwaltung")
    c1, _ = st.columns(2)

    project_def_json = get("projectdef", None)

    projectdefs = {
        f"{filter_name(d['customer'])}_{filter_name(d['project'])}_{filter_name(d['task'])}": d["id"]
        for d in project_def_json
    }

    projectdef = c1.selectbox(
        "Projekt Definition",
        options=projectdefs.keys(),
    )

    project_def_id = projectdefs[projectdef]

    if s.groups == "TL":
        with st.expander("Projekt anlegen oder bearbeiten?"):
            with st.form(f"frm"):
                customer_col, project_col, task_col = st.columns(3)
                start_col, end_col, _ = st.columns(3)
                budget_col, factor_col, _ = st.columns(3)

                api_calls = []

                # customer field
                with customer_col:
                    api_calls.append(
                        edit_field(
                            name="Kunde",
                            defaults=[projectdef.split("_")[0]],
                            endpoint="customer",
                        )
                    )

                # project field
                with project_col:
                    api_calls.append(
                        edit_field(
                            name="Projekt",
                            defaults=[projectdef.split("_")[1]],
                            endpoint="project",
                        )
                    )

                # task field
                with task_col:
                    api_calls.append(
                        edit_field(
                            name="Aufgabe",
                            defaults=[projectdef.split("_")[2]],
                            endpoint="task",
                        )
                    )

                # startdate field
                with start_col:
                    startdate = st.date_input("Projektstart")

                # enddate field
                with end_col:
                    enddate = st.date_input("Projektende")

                # budget field
                with budget_col:
                    budget = st.number_input("Budget", min_value=0.0, max_value=None)

                # factor field
                with factor_col:
                    factor = st.number_input("Faktor", min_value=1.0, max_value=None)

                # workers / participating employees field
                workers_data = {worker["uid"]: worker["name"] for worker in get("user/all")}
                selected_workers = st.multiselect("Mitarbeiter", options=workers_data.values())
                # TODO: filter machine users / API keys
                worker_ids = [key for key, value in workers_data.items() if value in selected_workers]

                # department field
                department_data = {department["id"]: department["label"] for department in get("department")}
                selected_department = st.selectbox("Abteilung", options=department_data.values())
                department_id = [key for key, value in department_data.items() if value == selected_department]

                # description field
                description = st.text_area("Projektbeschreibung")

                if st.form_submit_button("Save"):
                    request_results = {}
                    default_name = ""
                    for endpoint, data in api_calls:
                        submit_data = {"label": data[0] if data[0] else "NaN"}
                        response = post(endpoint=endpoint, data=submit_data)
                        request_results[f"{endpoint}_id"] = response["id"]
                        if not response["label"] == "NaN":
                            default_name = default_name + response["label"] + "_"

                    additional_data = {
                        "start": str(startdate),
                        "end": str(enddate),
                        "budget": budget,
                        "department_id": department_id,
                        "factor": factor,
                        "description": description,
                        "worker_ids": worker_ids,
                    }
                    request_results = {**request_results, **additional_data}

                    pjd_response = post(endpoint="projectdef", data=request_results)

                    if len(pjd_response) > 0:
                        st.success("Projekt erfolgreich angelegt / bearbeitet!")
                    else:
                        st.error("Projekt konnte nicht angelegt werden")

                    tag_submit_data = {
                        "project_def_id": pjd_response["id"],
                        "label": default_name[:-1],
                    }
                    tag_response = post("tag", data=tag_submit_data)

                    if len(tag_response) > 0:
                        st.success("Default Hashtag erfolgreich angelegt / bearbeitet!")
                    else:
                        st.error("Default Hashtag konnte nicht angelegt werden")
                    st.experimental_rerun()

    with st.form("Tags"):
        result = edit_field(
            name="Hashtags",
            endpoint="tag",
            maxtags=-1,
            filt=f"{project_def_id}/projects",
        )
        if st.form_submit_button("Save"):
            submit_data = {
                # "submitter_id": s.uid,
                "project_def_id": project_def_id,
                "label": result[-1],
            }
            response = post("tag", query=f"synonyms/{project_def_id}", data=submit_data)
            if response:
                if response["num_created"] > 0 or response["num_deleted"] > 0:
                    st.success(
                        f"Es wurden {response['num_created']} {'neue Hashtags' if response['num_created'] != 1 else 'neuer Hashtag'} angelegt und {response['num_deleted']} {'existierende Hashtags' if response['num_deleted'] != 1 else 'existierender Hashtag'} gelöscht"
                    )
                else:
                    st.warning("Es wurde keine Änderung vorgenommen.")
            else:
                st.error("Es ist etwas schiefgelaufen.")

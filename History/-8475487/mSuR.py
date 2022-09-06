import plotly.express as px
import streamlit as st

from app.core.auth import Session
from app.pages.calendar import load_cal_by_sql


def app() -> None:
    """Run projecthours page"""
    st.title("📈 Projektzeiten Übersicht  ")
    s = Session()

    # page = st.sidebar.selectbox("Navigation", self.pages, format_func=lambda page: page["title"])
    # select the project that you want extra information of
    # typeSelection = st.selectbox("Projekt Auswahl", format_func=lambda proj: )
    df = load_cal_by_sql(s.uid)
    df = df.dropna()

    fig = px.pie(
        df,
        values="duration",
        names="project",
        title="Prozentualer Anteil der geleisteten Stunden",
    )
    st.plotly_chart(fig)
    st.plotly_chart(fig)
    st.plotly_chart(fig)

import plotly.express as px
import streamlit as st

from app.core.auth import Session
from app.pages2.calendar import load_cal_by_sql


def app() -> None:
    """Run projecthours page"""
    st.title("📈 Projektstunden")
    s = Session()

    df = load_cal_by_sql(s.uid)
    df = df.dropna()

    fig = px.pie(
        df,
        values="duration",
        names="project",
        title="Prozentualer Anteil der geleisteten Stunden",
    )
    st.plotly_chart(fig)

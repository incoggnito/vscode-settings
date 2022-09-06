import streamlit as st
import pandas as pd

from app.core.auth import Session
from app.core.api import get


def app() -> None:
    """Run projecthours page"""
    st.title("📇 Projektstatistik")
    s = Session()

    df = pd.DataFrame(get("view/"))

    df.budget / (df.hourrate * df.factor * df.duration_sum)
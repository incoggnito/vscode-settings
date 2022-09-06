import streamlit as st

from app.core.auth import Session
from app.core.api import get

def app() -> None:
    """Run projecthours page"""
    st.title("📇 Projektstatistik")
    s = Session()

    r = get("view/")
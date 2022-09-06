import streamlit as st
import pandas as pd

from app.core.auth import Session
from app.core.api import get


def app() -> None:
    """Run projecthours page"""
    st.title("📇 Projektstatistik")
    s = Session()
    r = get("view")
    df = pd.DataFrame(r)
    df = df.dropna()
    df = df.groupby("pid").agg(
        {"duration_sum": "sum", "budget": "first", "factor": "first", "hourrate": "first", "projekt": "first"}
    )
    df["costs"] = df.hourrate * df.factor * df.duration_sum
    for _, row in df.iterrows():
        st.metric(label=row["project"], value=row["budget"], delta=row["costs"])
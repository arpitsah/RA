from __future__ import annotations

import pandas as pd
import streamlit as st

from app.auth import auth_widget, require_login
from app.persistence import list_reports_for_user

st.set_page_config(page_title="Saved Reports", layout="wide")
auth_widget()
st.title("Saved Reports")

if not require_login():
    st.stop()

reports = list_reports_for_user(st.session_state["user"])
if not reports:
    st.info("No saved reports yet.")
else:
    st.dataframe(pd.DataFrame(reports))

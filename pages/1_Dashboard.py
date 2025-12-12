# 1_Dashboard.py  (inside week9_app/pages)

import sys
from pathlib import Path

# --- Make sure Python can see the project root so "app" package works ---
ROOT_DIR = Path(__file__).resolve().parents[2]   # .../CW2_M0106.../
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd

from app.data.db import connect_database

# ----------------- Session / login guard -----------------

st.set_page_config(page_title="Dashboard", layout="wide")

# Make sure keys exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# If not logged in, send user back to Home
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

# ----------------- Load data from your SQLite DB -----------------

conn = connect_database()

# All incidents table
incidents_df = pd.read_sql_query(
    "SELECT id, date, incident_type, severity, status, description "
    "FROM cyber_incidents",
    conn,
)

conn.close()

# ----------------- Page layout -----------------

st.title("Dashboard")
st.success(f"Hello, {st.session_state.username}! You are logged in.")

st.caption("This dashboard shows data from the cyber_incidents table.")

# ----- Sidebar filters -----
with st.sidebar:
    st.header("Filters")

    severities = sorted(incidents_df["severity"].dropna().unique())
    statuses = sorted(incidents_df["status"].dropna().unique())

    selected_severity = st.multiselect(
        "Severity", options=severities, default=severities
    )
    selected_status = st.multiselect(
        "Status", options=statuses, default=statuses
    )

    show_table = st.checkbox("Show full incidents table", value=True)

# Apply filters
filtered_incidents = incidents_df[
    incidents_df["severity"].isin(selected_severity)
    & incidents_df["status"].isin(selected_status)
]

# ----- Top-level metrics -----
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total incidents", len(incidents_df))
with col2:
    st.metric("Filtered incidents", len(filtered_incidents))
with col3:
    high_count = (filtered_incidents["severity"] == "High").sum()
    st.metric("High-severity (filtered)", int(high_count))

st.divider()

# ----- Charts -----
st.subheader("Incidents by severity")

severity_counts = (
    filtered_incidents["severity"].value_counts()
    .sort_index()
    .rename_axis("severity")
    .reset_index(name="count")
)
st.bar_chart(severity_counts.set_index("severity"))

st.subheader("Incidents by status")

status_counts = (
    filtered_incidents["status"].value_counts()
    .sort_index()
    .rename_axis("status")
    .reset_index(name="count")
)
st.bar_chart(status_counts.set_index("status"))

st.divider()

# ----- Tables -----
st.subheader("Recent Incidents")

if show_table:
    st.dataframe(filtered_incidents)
else:
    st.info("Enable 'Show full incidents table' in the sidebar to see the table.")

with st.expander("See raw data (unfiltered)"):
    st.dataframe(incidents_df)

st.divider()

# ----- Logout -----
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")


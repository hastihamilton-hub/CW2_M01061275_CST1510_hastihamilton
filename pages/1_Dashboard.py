# pages/1_Dashboard.py

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
from app.data.db import connect_database


# ----------------- Page config -----------------
st.set_page_config(page_title="Dashboard", layout="wide")


# ----------------- Login guard -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()


# ----------------- Load data from SQLite -----------------
@st.cache_data(show_spinner=False)
def load_incidents():
    conn = connect_database()
    df = pd.read_sql_query(
        """
        SELECT id, date, incident_type, severity, status, description
        FROM cyber_incidents
        ORDER BY id DESC
        """,
        conn,
    )
    conn.close()
    return df


incidents_df = load_incidents()


# ----------------- Title + Intro -----------------
st.title("Incident Dashboard")

st.markdown(
    """
**What this page shows**
- This dashboard loads real records from the **cyber_incidents** table in the SQLite database.
- You can filter incidents by **severity** and **status**, search through descriptions, and view simple charts.
- The goal is to demonstrate **Streamlit multipage apps + data visualisation + database integration**.
"""
)

st.caption(f"Logged in as: {st.session_state.username}")
st.divider()


# ----------------- Sidebar: navigation + filters -----------------
with st.sidebar:
    st.header("Navigation")

    if st.button("AI Chat", use_container_width=True):
        st.switch_page("pages/ai_chat.py")

    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")

    st.divider()
    st.header("Filters")

    severities = sorted(incidents_df["severity"].dropna().unique().tolist())
    statuses = sorted(incidents_df["status"].dropna().unique().tolist())
    types = sorted(incidents_df["incident_type"].dropna().unique().tolist())

    selected_severity = st.multiselect("Severity", options=severities, default=severities)
    selected_status = st.multiselect("Status", options=statuses, default=statuses)

    search_text = st.text_input("Search in description (optional)", value="")

    sort_option = st.selectbox(
        "Sort by",
        ["Newest first (ID)", "Oldest first (ID)", "Severity A-Z", "Status A-Z"],
        index=0,
    )

    show_table = st.checkbox("Show filtered table", value=True)
    show_raw = st.checkbox("Show raw data", value=False)


# ----------------- Apply filters -----------------
filtered = incidents_df[
    incidents_df["severity"].isin(selected_severity)
    & incidents_df["status"].isin(selected_status)
].copy()

if search_text.strip():
    filtered = filtered[filtered["description"].str.contains(search_text, case=False, na=False)]


# ----------------- Sorting -----------------
if sort_option == "Newest first (ID)":
    filtered = filtered.sort_values("id", ascending=False)
elif sort_option == "Oldest first (ID)":
    filtered = filtered.sort_values("id", ascending=True)
elif sort_option == "Severity A-Z":
    filtered = filtered.sort_values("severity", ascending=True)
elif sort_option == "Status A-Z":
    filtered = filtered.sort_values("status", ascending=True)


# ----------------- Metrics -----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total incidents", len(incidents_df))
with col2:
    st.metric("Filtered incidents", len(filtered))
with col3:
    high_count = int((filtered["severity"] == "High").sum())
    st.metric("High severity (filtered)", high_count)
with col4:
    open_count = int((filtered["status"].str.lower() == "open").sum()) if "status" in filtered else 0
    st.metric("Open (filtered)", open_count)

st.divider()


# ----------------- Charts -----------------
left, right = st.columns(2)

with left:
    st.subheader("Incidents by Severity")
    sev_counts = filtered["severity"].value_counts().sort_index()
    st.bar_chart(sev_counts)

with right:
    st.subheader("Incidents by Status")
    status_counts = filtered["status"].value_counts().sort_index()
    st.bar_chart(status_counts)

st.divider()


# ----------------- Extra insight (Top Types) -----------------
st.subheader("Top Incident Types (Filtered)")
type_counts = filtered["incident_type"].value_counts().head(5)

if len(type_counts) == 0:
    st.info("No records found with the selected filters.")
else:
    st.bar_chart(type_counts)

st.divider()


# ----------------- Table views -----------------
st.subheader("Recent Incidents")

if show_table:
    st.dataframe(filtered, use_container_width=True)
else:
    st.info("Enable 'Show filtered table' in the sidebar to see the incident table.")

if show_raw:
    st.subheader("Raw Data (Unfiltered)")
    st.dataframe(incidents_df, use_container_width=True)

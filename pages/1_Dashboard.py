# ============================================================
# Multi-Domain Intelligence Platform – Dashboard Page
# This page visualizes data from all three domains:
# 1) Cybersecurity
# 2) Data Science
# 3) IT Operations
#
# Access to this page is restricted to logged-in users only.
# ============================================================

import sys
from pathlib import Path

# ------------------------------------------------------------
# Ensure project root is available for imports
# This allows access to shared modules (e.g. database connection)
# ------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
from app.data.db import connect_database


# ------------------------------------------------------------
# Page configuration
# Wide layout is used to better display dashboards and charts
# ------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Domain Dashboard",
    layout="wide"
)


# ------------------------------------------------------------
# Session validation (protected page)
# Prevents unauthenticated access to the dashboard
# ------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()


# ------------------------------------------------------------
# Load data from the SQLite database
# Data is cached to improve performance
# ------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_tables():
    """
    Loads all domain tables from the database.

    Returns:
        cyber_incidents (DataFrame)
        datasets_metadata (DataFrame)
        it_tickets (DataFrame)
    """
    conn = connect_database()

    cyber_incidents = pd.read_sql_query(
        """
        SELECT id, date, incident_type, severity, status, description, reported_by
        FROM cyber_incidents
        ORDER BY id DESC
        """,
        conn
    )

    datasets_metadata = pd.read_sql_query(
        """
        SELECT id, dataset_name, category, source, last_updated, record_count, file_size_mb
        FROM datasets_metadata
        ORDER BY id DESC
        """,
        conn
    )

    it_tickets = pd.read_sql_query(
        """
        SELECT id, priority, status, category, subject, description,
               created_date, resolved_date, assigned_to
        FROM it_tickets
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()
    return cyber_incidents, datasets_metadata, it_tickets


# Load all domain datasets
incidents_df, datasets_df, tickets_df = load_tables()


# ------------------------------------------------------------
# Sidebar: Navigation and global controls
# ------------------------------------------------------------
with st.sidebar:
    st.header("Navigation")

    # Navigate to AI chat page
    if st.button("AI Chat", use_container_width=True):
        st.switch_page("pages/ai_chat.py")

    # Logout button
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")

    st.divider()

    # Global display controls
    st.header("Display Options")
    show_raw_tables = st.checkbox("Show raw data tables", value=False)
    max_rows = st.slider("Rows to display", 10, 500, 100)


# ------------------------------------------------------------
# Page title and introduction
# ------------------------------------------------------------
st.title("Multi-Domain Intelligence Platform Dashboard")
st.caption(f"Logged in as: {st.session_state.username}")

st.markdown(
    """
This dashboard presents a **unified view of three operational domains**:

- **Cybersecurity** — monitoring security incidents and threats
- **Data Science** — managing datasets and metadata
- **IT Operations** — tracking IT support tickets

The data is loaded directly from a SQLite database and visualized using
interactive charts, filters, and tables.
"""
)

st.divider()


# ------------------------------------------------------------
# High-level KPI metrics
# ------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Cyber Incidents", len(incidents_df))

with k2:
    st.metric("Datasets", len(datasets_df))

with k3:
    st.metric("IT Tickets", len(tickets_df))

with k4:
    open_incidents = (incidents_df["status"].astype(str).str.lower() == "open").sum()
    open_tickets = (tickets_df["status"].astype(str).str.lower() == "open").sum()
    st.metric("Open Issues", int(open_incidents + open_tickets))


st.divider()


# ------------------------------------------------------------
# Domain Tabs
# ------------------------------------------------------------
tab_overview, tab_cyber, tab_data, tab_it = st.tabs(
    ["Overview", "Cybersecurity", "Data Science", "IT Operations"]
)


# =========================
# OVERVIEW TAB
# =========================
with tab_overview:
    st.subheader("System Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.caption("Cyber incidents by severity")
        st.bar_chart(incidents_df["severity"].value_counts().sort_index())

    with col2:
        st.caption("IT tickets by priority")
        st.bar_chart(tickets_df["priority"].value_counts().sort_index())

    if show_raw_tables:
        st.divider()
        st.subheader("Raw Data Preview")
        st.dataframe(incidents_df.head(max_rows))
        st.dataframe(datasets_df.head(max_rows))
        st.dataframe(tickets_df.head(max_rows))


# =========================
# CYBERSECURITY TAB
# =========================
with tab_cyber:
    st.subheader("Cybersecurity Incidents")

    with st.expander("Filters", expanded=True):
        severities = sorted(incidents_df["severity"].dropna().unique())
        statuses = sorted(incidents_df["status"].dropna().unique())

        f_sev = st.multiselect("Severity", severities, default=severities)
        f_status = st.multiselect("Status", statuses, default=statuses)

    filtered = incidents_df[
        incidents_df["severity"].isin(f_sev)
        & incidents_df["status"].isin(f_status)
    ]

    st.metric("Filtered Incidents", len(filtered))
    st.bar_chart(filtered["incident_type"].value_counts())

    st.dataframe(filtered.head(max_rows), use_container_width=True)


# =========================
# DATA SCIENCE TAB
# =========================
with tab_data:
    st.subheader("Dataset Metadata")

    datasets_df["record_count"] = pd.to_numeric(
        datasets_df["record_count"], errors="coerce"
    ).fillna(0)

    st.metric("Total Records", int(datasets_df["record_count"].sum()))

    st.bar_chart(
        datasets_df.sort_values("record_count", ascending=False)
        .head(10)
        .set_index("dataset_name")["record_count"]
    )

    st.dataframe(datasets_df.head(max_rows), use_container_width=True)


# =========================
# IT OPERATIONS TAB
# =========================
with tab_it:
    st.subheader("IT Support Tickets")

    with st.expander("Filters", expanded=True):
        priorities = sorted(tickets_df["priority"].dropna().unique())
        statuses = sorted(tickets_df["status"].dropna().unique())

        f_pr = st.multiselect("Priority", priorities, default=priorities)
        f_st = st.multiselect("Status", statuses, default=statuses)

    it_filtered = tickets_df[
        tickets_df["priority"].isin(f_pr)
        & tickets_df["status"].isin(f_st)
    ]

    st.metric("Filtered Tickets", len(it_filtered))
    st.bar_chart(it_filtered["priority"].value_counts())

    st.dataframe(it_filtered.head(max_rows), use_container_width=True)

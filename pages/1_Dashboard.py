# ============================================================
# Multi-Domain Intelligence Platform – Dashboard Page
#
# This Streamlit page provides a unified dashboard for:
#   1) Cybersecurity (incident monitoring)
#   2) Data Science (dataset metadata analysis)
#   3) IT Operations (ticket tracking)
#
# Access to this page is restricted to authenticated users.
# ============================================================

# -----------------------------
# Standard library imports
# -----------------------------
import sys
from pathlib import Path

# Ensure the project root directory is on Python's import path.
# This allows Streamlit multipage apps to import internal modules correctly.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# -----------------------------
# Third-party imports
# -----------------------------
import streamlit as st
import pandas as pd

# -----------------------------
# Internal project imports
# -----------------------------
from app.data.db import connect_database


# ============================================================
# Helper Functions
# ============================================================

def require_login():
    """
    Guard function to prevent unauthorized access.

    If the user is not logged in, this function:
    - Displays an error message
    - Provides a button to return to the login page
    - Stops further execution of the page
    """
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    if not st.session_state.logged_in:
        st.error("You must be logged in to view the dashboard.")
        if st.button("Go to login page"):
            st.switch_page("Home.py")
        st.stop()


def load_tables():
    """
    Load all three domain tables from the SQLite database.

    Returns:
        tuple: (cybersecurity incidents, datasets metadata, IT tickets)
               as pandas DataFrames
    """
    conn = connect_database()

    # Cybersecurity incidents table
    incidents_df = pd.read_sql_query(
        """
        SELECT id, date, incident_type, severity, status, description
        FROM cyber_incidents
        ORDER BY id DESC
        """,
        conn,
    )

    # Data science datasets metadata table
    datasets_df = pd.read_sql_query(
        """
        SELECT id, dataset_name, category, source, last_updated,
               record_count, file_size_mb
        FROM datasets_metadata
        ORDER BY id DESC
        """,
        conn,
    )

    # IT operations tickets table
    tickets_df = pd.read_sql_query(
        """
        SELECT id, priority, status, category, subject, description,
               created_date, resolved_date, assigned_to
        FROM it_tickets
        ORDER BY id DESC
        """,
        conn,
    )

    conn.close()
    return incidents_df, datasets_df, tickets_df


def safe_str_series(df, col):
    """
    Safely convert a DataFrame column to string type.

    This avoids issues caused by NULL values or mixed data types
    when applying filters in Streamlit widgets.
    """
    if col not in df.columns:
        return pd.Series([], dtype="string")
    return df[col].astype("string").fillna("")


# ============================================================
# Page Setup
# ============================================================

st.set_page_config(
    page_title="Tier 3 Dashboard",
    page_icon="📊",
    layout="wide"
)

# Enforce login before showing any data
require_login()

# Load all domain data
incidents_df, datasets_df, tickets_df = load_tables()

# Page title and user context
st.title("Multi-Domain Intelligence Platform Dashboard")
st.caption(f"Logged in as: {st.session_state.username}")

# Introductory explanation for the dashboard
st.markdown(
    """
This dashboard integrates **three operational domains** into a single interface:

- **Cybersecurity:** Monitor incidents, severity, and response status  
- **Data Science:** Explore dataset metadata, sources, and record volumes  
- **IT Operations:** Track support tickets, priorities, and workload  

The goal is to demonstrate how multiple data domains can be securely combined,
analysed, and visualised in a real-world system.
"""
)

# ============================================================
# Sidebar Controls
# ============================================================

with st.sidebar:
    st.header("Navigation")

    # Link to AI chat assistant
    if st.button("AI Chat", use_container_width=True):
        st.switch_page("pages/ai_chat.py")

    st.divider()
    st.header("Dashboard Filters")

    # -----------------------------
    # Cybersecurity filters
    # -----------------------------
    st.subheader("Cybersecurity")

    incident_severities = sorted(
        safe_str_series(incidents_df, "severity").dropna().unique().tolist()
    )
    incident_statuses = sorted(
        safe_str_series(incidents_df, "status").dropna().unique().tolist()
    )

    selected_severity = st.multiselect(
        "Severity",
        options=incident_severities,
        default=incident_severities,
    )

    selected_inc_status = st.multiselect(
        "Status",
        options=incident_statuses,
        default=incident_statuses,
    )

    # -----------------------------
    # IT Operations filters
    # -----------------------------
    st.subheader("IT Operations")

    ticket_priorities = sorted(
        safe_str_series(tickets_df, "priority").dropna().unique().tolist()
    )
    ticket_statuses = sorted(
        safe_str_series(tickets_df, "status").dropna().unique().tolist()
    )

    selected_ticket_priority = st.multiselect(
        "Ticket priority",
        options=ticket_priorities,
        default=ticket_priorities,
    )

    selected_ticket_status = st.multiselect(
        "Ticket status",
        options=ticket_statuses,
        default=ticket_statuses,
    )

    st.divider()
    show_raw = st.checkbox("Show raw tables", value=False)

    st.divider()
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")


# ============================================================
# Apply Filters
# ============================================================

# Filter cybersecurity incidents
filtered_incidents = incidents_df[
    incidents_df["severity"].astype("string").isin(selected_severity)
    & incidents_df["status"].astype("string").isin(selected_inc_status)
].copy()

# Filter IT tickets
filtered_tickets = tickets_df[
    tickets_df["priority"].astype("string").isin(selected_ticket_priority)
    & tickets_df["status"].astype("string").isin(selected_ticket_status)
].copy()


# ============================================================
# KPI Summary Row
# ============================================================

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.metric("Incidents", len(incidents_df))
with k2:
    st.metric("Incidents (filtered)", len(filtered_incidents))
with k3:
    st.metric("Datasets", len(datasets_df))
with k4:
    total_records = (
        pd.to_numeric(datasets_df.get("record_count", pd.Series([])),
                      errors="coerce")
        .fillna(0)
        .sum()
    )
    st.metric("Total records", int(total_records))
with k5:
    st.metric("Tickets", len(tickets_df))
with k6:
    st.metric("Tickets (filtered)", len(filtered_tickets))

st.divider()


# ============================================================
# SECTION 1: CYBERSECURITY
# ============================================================

st.header("1) Cybersecurity Domain")
st.caption("Incident monitoring and risk analysis.")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Incidents by severity")
    sev_counts = (
        filtered_incidents["severity"].astype("string")
        .value_counts()
        .rename_axis("severity")
        .reset_index(name="count")
    )
    if sev_counts.empty:
        st.info("No incidents match the current filters.")
    else:
        st.bar_chart(sev_counts.set_index("severity"))

with c2:
    st.subheader("Incidents by status")
    status_counts = (
        filtered_incidents["status"].astype("string")
        .value_counts()
        .rename_axis("status")
        .reset_index(name="count")
    )
    if status_counts.empty:
        st.info("No incidents match the current filters.")
    else:
        st.bar_chart(status_counts.set_index("status"))

st.subheader("Recent incidents")
st.dataframe(filtered_incidents.head(50), use_container_width=True)


# ============================================================
# SECTION 2: DATA SCIENCE
# ============================================================

st.divider()
st.header("2) Data Science Domain")
st.caption("Dataset catalog overview and analytics.")

d1, d2 = st.columns(2)

with d1:
    st.subheader("Top datasets by record count")
    ds = datasets_df.copy()
    ds["record_count"] = pd.to_numeric(ds["record_count"], errors="coerce").fillna(0)
    top_records = ds.sort_values("record_count", ascending=False).head(10)

    if top_records.empty:
        st.info("No dataset metadata available.")
    else:
        st.bar_chart(
            top_records[["dataset_name", "record_count"]].set_index("dataset_name")
        )

with d2:
    st.subheader("Datasets by source")
    source_counts = (
        datasets_df["source"].astype("string")
        .fillna("Unknown")
        .value_counts()
        .rename_axis("source")
        .reset_index(name="count")
    )

    if source_counts.empty:
        st.info("No dataset sources found.")
    else:
        st.bar_chart(source_counts.set_index("source"))

st.subheader("Dataset catalog")
st.dataframe(datasets_df.head(50), use_container_width=True)


# ============================================================
# SECTION 3: IT OPERATIONS
# ============================================================

st.divider()
st.header("3) IT Operations Domain")
st.caption("Support ticket tracking and workload overview.")

t1, t2 = st.columns(2)

with t1:
    st.subheader("Tickets by priority")
    priority_counts = (
        filtered_tickets["priority"].astype("string")
        .value_counts()
        .rename_axis("priority")
        .reset_index(name="count")
    )
    if priority_counts.empty:
        st.info("No tickets match the current filters.")
    else:
        st.bar_chart(priority_counts.set_index("priority"))

with t2:
    st.subheader("Tickets by status")
    ticket_status_counts = (
        filtered_tickets["status"].astype("string")
        .value_counts()
        .rename_axis("status")
        .reset_index(name="count")
    )
    if ticket_status_counts.empty:
        st.info("No tickets match the current filters.")
    else:
        st.bar_chart(ticket_status_counts.set_index("status"))

st.subheader("Recent tickets")
st.dataframe(filtered_tickets.head(50), use_container_width=True)


# ============================================================
# Optional Raw Data Tables
# ============================================================

if show_raw:
    st.divider()
    st.subheader("Raw database tables")

    with st.expander("cyber_incidents"):
        st.dataframe(incidents_df, use_container_width=True)

    with st.expander("datasets_metadata"):
        st.dataframe(datasets_df, use_container_width=True)

    with st.expander("it_tickets"):
        st.dataframe(tickets_df, use_container_width=True)

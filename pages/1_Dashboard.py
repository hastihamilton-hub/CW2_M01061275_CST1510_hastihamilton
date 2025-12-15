# ============================================================
# Multi-Domain Intelligence Platform – Dashboard Page
# This page visualizes data from all three domains:
# 1) Cybersecurity
# 2) Data Science
# 3) IT Operations
#
# Access to this page is restricted to logged-in users only.
# ============================================================

# pages/1_Dashboard.py
# Tier 3 Dashboard: Cybersecurity + Data Science + IT Operations

import sys
from pathlib import Path

# Make sure we can import from the project root when running as a Streamlit multipage app
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd

from app.data.db import connect_database


# -----------------------------
# Helpers
# -----------------------------
def require_login():
    """Block access if the user is not logged in."""
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
    """Load all three domain tables from SQLite into DataFrames."""
    conn = connect_database()

    incidents_df = pd.read_sql_query(
        """
        SELECT id, date, incident_type, severity, status, description
        FROM cyber_incidents
        ORDER BY id DESC
        """,
        conn,
    )

    datasets_df = pd.read_sql_query(
        """
        SELECT id, dataset_name, category, source, last_updated, record_count, file_size_mb
        FROM datasets_metadata
        ORDER BY id DESC
        """,
        conn,
    )

    tickets_df = pd.read_sql_query(
        """
        SELECT id, priority, status, category, subject, description, created_date, resolved_date, assigned_to
        FROM it_tickets
        ORDER BY id DESC
        """,
        conn,
    )

    conn.close()
    return incidents_df, datasets_df, tickets_df


def safe_str_series(df, col):
    """Return a string Series (avoids issues if column has nulls/numbers)."""
    if col not in df.columns:
        return pd.Series([], dtype="string")
    return df[col].astype("string").fillna("")


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Tier 3 Dashboard", page_icon="📊", layout="wide")
require_login()

incidents_df, datasets_df, tickets_df = load_tables()

st.title("Multi-Domain Intelligence Platform Dashboard")
st.caption(f"Logged in as: {st.session_state.username}")

st.markdown(
    """
This dashboard demonstrates **three integrated domains** from the project database:

- **Cybersecurity:** incident monitoring and severity/status analysis  
- **Data Science:** dataset catalog insights (records, sources, update dates)  
- **IT Operations:** ticket tracking by priority/status and workload overview
"""
)

# -----------------------------
# Sidebar controls (global)
# -----------------------------
with st.sidebar:
    st.header("Navigation")
    if st.button("AI Chat", use_container_width=True):
        st.switch_page("pages/ai_chat.py")

    st.divider()
    st.header("Dashboard Filters")

    st.subheader("Cybersecurity")
    incident_severities = sorted(safe_str_series(incidents_df, "severity").dropna().unique().tolist())
    incident_statuses = sorted(safe_str_series(incidents_df, "status").dropna().unique().tolist())

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

    st.subheader("IT Operations")
    ticket_priorities = sorted(safe_str_series(tickets_df, "priority").dropna().unique().tolist())
    ticket_statuses = sorted(safe_str_series(tickets_df, "status").dropna().unique().tolist())

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


# -----------------------------
# Apply filters
# -----------------------------
filtered_incidents = incidents_df[
    incidents_df["severity"].astype("string").isin(selected_severity)
    & incidents_df["status"].astype("string").isin(selected_inc_status)
].copy()

filtered_tickets = tickets_df[
    tickets_df["priority"].astype("string").isin(selected_ticket_priority)
    & tickets_df["status"].astype("string").isin(selected_ticket_status)
].copy()


# -----------------------------
# Top KPI row (all domains)
# -----------------------------
k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.metric("Incidents", len(incidents_df))
with k2:
    st.metric("Incidents (filtered)", len(filtered_incidents))
with k3:
    st.metric("Datasets", len(datasets_df))
with k4:
    # total records (data science)
    rec_sum = pd.to_numeric(datasets_df.get("record_count", pd.Series([])), errors="coerce").fillna(0).sum()
    st.metric("Total records", int(rec_sum))
with k5:
    st.metric("Tickets", len(tickets_df))
with k6:
    st.metric("Tickets (filtered)", len(filtered_tickets))

st.divider()


# =========================================================
# SECTION 1: CYBERSECURITY
# =========================================================
st.header("1) Cybersecurity Domain")
st.caption("Incident monitoring and risk overview based on the cyber_incidents table.")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Incidents by severity")
    sev_counts = (
        filtered_incidents["severity"].astype("string").value_counts()
        .rename_axis("severity")
        .reset_index(name="count")
        .sort_values("severity")
    )
    if len(sev_counts) == 0:
        st.info("No incidents match the current filters.")
    else:
        st.bar_chart(sev_counts.set_index("severity"))

with c2:
    st.subheader("Incidents by status")
    status_counts = (
        filtered_incidents["status"].astype("string").value_counts()
        .rename_axis("status")
        .reset_index(name="count")
        .sort_values("status")
    )
    if len(status_counts) == 0:
        st.info("No incidents match the current filters.")
    else:
        st.bar_chart(status_counts.set_index("status"))

st.subheader("Recent incidents (filtered)")
st.dataframe(filtered_incidents.head(50), use_container_width=True)


# =========================================================
# SECTION 2: DATA SCIENCE
# =========================================================
st.divider()
st.header("2) Data Science Domain")
st.caption("Dataset catalog insights based on the datasets_metadata table.")

d1, d2 = st.columns(2)

with d1:
    st.subheader("Records by dataset (top 10)")
    ds = datasets_df.copy()
    ds["record_count"] = pd.to_numeric(ds["record_count"], errors="coerce").fillna(0)
    top_records = ds.sort_values("record_count", ascending=False).head(10)
    if len(top_records) == 0:
        st.info("No dataset metadata found.")
    else:
        chart_df = top_records[["dataset_name", "record_count"]].set_index("dataset_name")
        st.bar_chart(chart_df)

with d2:
    st.subheader("Datasets by source")
    src_counts = (
        datasets_df["source"].astype("string").fillna("Unknown").value_counts()
        .rename_axis("source")
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    if len(src_counts) == 0:
        st.info("No dataset sources found.")
    else:
        st.bar_chart(src_counts.set_index("source"))

st.subheader("Dataset catalog (latest)")
st.dataframe(datasets_df.head(50), use_container_width=True)


# =========================================================
# SECTION 3: IT OPERATIONS
# =========================================================
st.divider()
st.header("3) IT Operations Domain")
st.caption("Ticket workflow and workload overview based on the it_tickets table.")

t1, t2 = st.columns(2)

with t1:
    st.subheader("Tickets by priority")
    pr_counts = (
        filtered_tickets["priority"].astype("string").value_counts()
        .rename_axis("priority")
        .reset_index(name="count")
        .sort_values("priority")
    )
    if len(pr_counts) == 0:
        st.info("No tickets match the current filters.")
    else:
        st.bar_chart(pr_counts.set_index("priority"))

with t2:
    st.subheader("Tickets by status")
    tk_status_counts = (
        filtered_tickets["status"].astype("string").value_counts()
        .rename_axis("status")
        .reset_index(name="count")
        .sort_values("status")
    )
    if len(tk_status_counts) == 0:
        st.info("No tickets match the current filters.")
    else:
        st.bar_chart(tk_status_counts.set_index("status"))

st.subheader("Recent tickets (filtered)")
st.dataframe(filtered_tickets.head(50), use_container_width=True)


# -----------------------------
# Optional raw tables
# -----------------------------
if show_raw:
    st.divider()
    st.subheader("Raw tables (unfiltered)")
    with st.expander("cyber_incidents"):
        st.dataframe(incidents_df, use_container_width=True)
    with st.expander("datasets_metadata"):
        st.dataframe(datasets_df, use_container_width=True)
    with st.expander("it_tickets"):
        st.dataframe(tickets_df, use_container_width=True)

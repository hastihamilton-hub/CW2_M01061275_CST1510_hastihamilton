import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
from openai import OpenAI

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="wide",
)

# ----------------------------
# Guard: must be logged in
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.error("You must be logged in to use the AI Chat.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# ----------------------------
# Load API key from secrets
# ----------------------------
# Create .streamlit/secrets.toml with:
# OPENAI_API_KEY = "your_key"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ----------------------------
# Sidebar controls
# ----------------------------
with st.sidebar:
    st.title("🤖 AI Settings")

    mode = st.selectbox(
        "Assistant mode",
        ["General", "Cybersecurity", "Data Science", "IT Support"],
        index=0,
    )

    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0,
    )

    temperature = st.slider(
        "Creativity (temperature)",
        0.0, 2.0, 0.7, 0.1
    )

    st.divider()

    if st.button("🗑 Clear chat", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()

# ----------------------------
# System prompts (looks impressive)
# ----------------------------
SYSTEM_PROMPTS = {
    "General": "You are a helpful assistant. Explain clearly and politely.",
    "Cybersecurity": (
        "You are a cybersecurity assistant. Give structured answers with practical steps, "
        "mention common threats, mitigations, and best practices."
    ),
    "Data Science": (
        "You are a data science assistant. Help with analysis ideas, visualization, "
        "and explain concepts simply with examples."
    ),
    "IT Support": (
        "You are an IT support assistant. Troubleshoot step-by-step and suggest the most likely fixes first."
    ),
}

# ----------------------------
# Title
# ----------------------------
st.title("💬 AI Chat")
st.caption(f"Logged in as **{st.session_state.username}** • Mode: **{mode}**")

# ----------------------------
# Chat session state
# ----------------------------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Build message list for the API (include system prompt first)
api_messages = [{"role": "system", "content": SYSTEM_PROMPTS[mode]}]
api_messages += st.session_state.chat_messages

# ----------------------------
# Display previous messages
# ----------------------------
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# Input box
# ----------------------------
prompt = st.chat_input("Type a message...")

if prompt:
    # Show user message immediately
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant reply (streaming)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_reply = ""

        try:
            stream = client.chat.completions.create(
                model=model,
                messages=api_messages + [{"role": "user", "content": prompt}],
                temperature=temperature,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    full_reply += delta.content
                    placeholder.markdown(full_reply + "▌")

            placeholder.markdown(full_reply)

        except Exception as e:
            full_reply = f"⚠️ Error: {e}"
            placeholder.markdown(full_reply)

    # Save assistant reply
    st.session_state.chat_messages.append({"role": "assistant", "content": full_reply})

# ----------------------------
# Quick navigation buttons
# ----------------------------
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅ Back to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
with col2:
    if st.button("🚪 Log out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")

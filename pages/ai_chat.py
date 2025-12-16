import sys
from pathlib import Path

# -------------------------------------------------
# Ensure project root is available in Python path
# This allows imports like app.services, app.data, etc.
# -------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
from openai import OpenAI


# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="wide",
)


# -------------------------------------------------
# Access control: user must be logged in
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Block access if user is not authenticated
if not st.session_state.logged_in:
    st.error("You must be logged in to use the AI Chat.")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()


# -------------------------------------------------
# OpenAI client setup
# API key is securely loaded from Streamlit secrets
# -------------------------------------------------
# secrets.toml example:
# OPENAI_API_KEY = "your_api_key_here"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# -------------------------------------------------
# Sidebar controls (AI configuration)
# -------------------------------------------------
with st.sidebar:
    st.title("🤖 AI Settings")

    # Select the assistant behavior / domain
    mode = st.selectbox(
        "Assistant mode",
        ["General", "Cybersecurity", "Data Science", "IT Support"],
        index=0,
    )

    # Choose which OpenAI model to use
    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0,
    )

    # Control response creativity
    temperature = st.slider(
        "Creativity (temperature)",
        0.0, 2.0, 0.7, 0.1
    )

    st.divider()

    # Clear chat history button
    if st.button("🗑 Clear chat", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()


# -------------------------------------------------
# System prompts per assistant mode
# These define the AI's role and response style
# -------------------------------------------------
SYSTEM_PROMPTS = {
    "General": (
        "You are a helpful assistant. Explain clearly and politely."
    ),
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


# -------------------------------------------------
# Page header
# -------------------------------------------------
st.title("💬 AI Chat")
st.caption(
    f"Logged in as **{st.session_state.username}** • Mode: **{mode}**"
)


# -------------------------------------------------
# Chat session state
# Stores conversation history for the current session
# -------------------------------------------------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Build message list sent to OpenAI
# System prompt is always the first message
api_messages = [{"role": "system", "content": SYSTEM_PROMPTS[mode]}]
api_messages += st.session_state.chat_messages


# -------------------------------------------------
# Display previous chat messages
# -------------------------------------------------
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -------------------------------------------------
# User input box
# -------------------------------------------------
prompt = st.chat_input("Type a message...")

if prompt:
    # Store and display user message immediately
    st.session_state.chat_messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using streaming
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_reply = ""

        try:
            stream = client.chat.completions.create(
                model=model,
                messages=api_messages + [
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                stream=True,
            )

            # Stream response chunk-by-chunk
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    full_reply += delta.content
                    placeholder.markdown(full_reply + "▌")

            # Final response without cursor
            placeholder.markdown(full_reply)

        except Exception as e:
            # Graceful error handling
            full_reply = f"⚠️ Error: {e}"
            placeholder.markdown(full_reply)

    # Save assistant reply to session history
    st.session_state.chat_messages.append(
        {"role": "assistant", "content": full_reply}
    )


# -------------------------------------------------
# Navigation buttons
# -------------------------------------------------
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

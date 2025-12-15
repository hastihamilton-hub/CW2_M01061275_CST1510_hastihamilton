import streamlit as st

from app.services.user_service import register_user, login_user


st.set_page_config(
    page_title="Login / Register",
    page_icon="🔑",
    layout="centered",
)

# -----------------------------
# Session state (login only)
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🔐 Multi-Domain Intelligence Platform")
st.caption("Login or create an account to access the dashboard.")

# If already logged in, jump to dashboard
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📊 Go to Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
    with col_b:
        if st.button("💬 Go to AI Chat", use_container_width=True):
            st.switch_page("pages/ai_chat.py")
    st.stop()

# -----------------------------
# Tabs
# -----------------------------
tab_login, tab_register = st.tabs(["Login", "Register"])

# ----- LOGIN TAB -----
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary", use_container_width=True):
        success, msg = login_user(login_username, login_password)

        if success:
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(msg)
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error(msg)

# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    role = st.selectbox("Role (optional)", ["user", "analyst", "admin"], index=0)

    if st.button("Create account", use_container_width=True):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            success, msg = register_user(new_username, new_password, role)
            if success:
                st.success(msg)
                st.info("Now switch to the Login tab and sign in.")
            else:
                st.error(msg)

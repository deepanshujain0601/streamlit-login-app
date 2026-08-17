"""
Streamlit Login App
--------------------
A simple, self-contained authentication demo built with Streamlit.

Features:
- Login form with username + password
- Passwords are hashed (SHA-256) — never stored or compared in plain text
- Session persistence via st.session_state
- Protected "dashboard" page shown only after successful login
- Logout button that clears the session
- Basic error handling for invalid credentials
"""

import hashlib
import time
from datetime import datetime

import streamlit as st

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Login App",
    layout="centered",
)

# ----------------------------------------------------------------------
# "Database" — in a real app this would be a proper DB (Postgres, etc.)
# Passwords below are pre-hashed with SHA-256.
# demo_user  -> Demo@123
# admin      -> Admin@123
# ----------------------------------------------------------------------
def _hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


USER_DB = {
    "demo_user": {
        "password_hash": _hash("Demo@123"),
        "name": "Demo User",
        "role": "Member",
    },
    "admin": {
        "password_hash": _hash("Admin@123"),
        "name": "Admin",
        "role": "Administrator",
    },
}

MAX_ATTEMPTS = 3

# ----------------------------------------------------------------------
# Session state initialisation
# ----------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
if "login_time" not in st.session_state:
    st.session_state.login_time = None


def check_credentials(username: str, password: str) -> bool:
    user = USER_DB.get(username)
    if not user:
        return False
    return user["password_hash"] == _hash(password)


def login(username: str, password: str) -> bool:
    if check_credentials(username, password):
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.login_attempts = 0
        st.session_state.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return True
    st.session_state.login_attempts += 1
    return False


def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.login_attempts = 0
    st.session_state.login_time = None


# ----------------------------------------------------------------------
# UI: Login screen
# ----------------------------------------------------------------------
def render_login():
    st.title("Login")
    st.caption("Sign in to continue")

    if st.session_state.login_attempts >= MAX_ATTEMPTS:
        st.error("Too many failed attempts. Please wait and try again.")
        if st.button("Reset attempts"):
            st.session_state.login_attempts = 0
            st.rerun()
        return

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="e.g. demo_user")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Log in", use_container_width=True)

    if submitted:
        if not username or not password:
            st.warning("Please enter both username and password.")
        elif login(username, password):
            st.success("Login successful! Redirecting...")
            time.sleep(0.6)
            st.rerun()
        else:
            remaining = MAX_ATTEMPTS - st.session_state.login_attempts
            st.error(f"Invalid username or password. {remaining} attempt(s) remaining.")

    with st.expander("Demo credentials"):
        st.code("username: demo_user\npassword: Demo@123", language="text")
        st.code("username: admin\npassword: Admin@123", language="text")


# ----------------------------------------------------------------------
# UI: Dashboard (protected page)
# ----------------------------------------------------------------------
def render_dashboard():
    user = USER_DB[st.session_state.username]

    with st.sidebar:
        st.header("👤 Account")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Role:** {user['role']}")
        st.write(f"**Logged in at:** {st.session_state.login_time}")
        st.divider()
        if st.button("Log out", use_container_width=True):
            logout()
            st.rerun()

    st.title(f"Welcome, {user['name']}")
    st.caption(f"Role: {user['role']}")
    st.success("You have successfully logged in and reached the protected dashboard.")

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Sessions", "1")
    col2.metric("Account Role", user["role"])
    col3.metric("Status", "Verified")

    st.divider()
    st.subheader("Session details")
    st.json(
        {
            "username": st.session_state.username,
            "authenticated": st.session_state.authenticated,
            "login_time": st.session_state.login_time,
        }
    )


# ----------------------------------------------------------------------
# Router
# ----------------------------------------------------------------------
if st.session_state.authenticated:
    render_dashboard()
else:
    render_login()

# Streamlit Login App

A simple, self-contained login/authentication demo built with [Streamlit](https://streamlit.io).

## Features
- Username + password login form
- Passwords stored as SHA-256 hashes (never plain text)
- Session persistence with `st.session_state`
- Protected dashboard page shown only after successful login
- Failed-attempt limiting (locks after 3 wrong tries)
- Logout button that clears the session

## Demo credentials
| Username | Password |
|---|---|
| `demo_user` | `Demo@123` |
| `admin` | `Admin@123` |

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
The app will open at `http://localhost:8501`.

## Deployment
Deployed on [Streamlit Community Cloud](https://streamlit.io/cloud):
1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select this repo/branch, set the main file to `app.py`.
4. Click **Deploy**.

## Project structure
```
streamlit-login-app/
├── app.py                  # Main application
├── requirements.txt        # Python dependencies
├── .streamlit/config.toml  # Streamlit server config
└── README.md
```

import streamlit as st
import requests
import os

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Media App", layout="centered")

# =========================
# SESSION STATE
# =========================
if "token" not in st.session_state:
    st.session_state.token = None

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox(
    "Menu",
    ["Register", "Login", "Upload", "View Media"]
)

# =========================
# REGISTER
# =========================
if menu == "Register":
    st.title("Register")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        res = requests.post(
            f"{BASE_URL}/auth/register",
            json={"email": email, "password": password}
        )

        if res.status_code == 200:
            st.success("User created successfully")
        else:
            st.error(res.text)

# =========================
# LOGIN
# =========================
elif menu == "Login":
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )

        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
            st.success("Logged in successfully")
        else:
            st.error("Login failed")

# =========================
# UPLOAD
# =========================
elif menu == "Upload":
    st.title("Upload Media")

    if not st.session_state.token:
        st.warning("Please login first")
    else:
        description = st.text_input("Description")
        file = st.file_uploader("Upload Image/Video")

        if st.button("Upload"):
            if file:
                files = {
                    "file": (file.name, file.getvalue())
                }

                # IMPORTANT FIX — SEND AS QUERY PARAMETERS
                params = {
                    "token": st.session_state.token,
                    "description": description
                }

                res = requests.post(
                    f"{BASE_URL}/media/upload",
                    params=params,
                    files=files,
                )

                if res.status_code == 200:
                    st.success("Uploaded successfully")
                else:
                    st.error(res.text)

# =========================
# VIEW MEDIA
# =========================
elif menu == "View Media":
    st.title("Uploaded Media")

    res = requests.get(f"{BASE_URL}/media/")

    if res.status_code == 200:
        media_list = res.json()

        for media in media_list:
            st.write(media["description"])

            # Correct path based on your folder structure
            file_path = os.path.join("uploads", media["filename"])

            # Display
            if media["filename"].lower().endswith((".png", ".jpg", ".jpeg")):
                st.image(file_path)
            else:
                st.video(file_path)
    else:
        st.error("Failed to fetch media")
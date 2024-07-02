import streamlit as st
from supabase import create_client, Client
import os

# --- Supabase Configuration ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Ayurvedic Healthcare", page_icon="🌿")

# --- Initialize Session State ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None

# --- Home Screen UI ---
st.title("Welcome to Our Ayurvedic Healthcare Platform")
st.write("Discover holistic wellness through the power of Ayurveda.")

# --- User Authentication and Role Management ---
if st.session_state["logged_in"]:
    # User is already logged in, redirect based on role
    if st.session_state["user_role"] == "patient":
        st.success("You are logged in as a Patient!")
        st.button("Go to Patient Dashboard", on_click=lambda: st.session_state.update({"page": "patient_dashboard"}))
    elif st.session_state["user_role"] == "doctor":
        st.success("You are logged in as a Doctor!")
        st.button("Go to Doctor Dashboard", on_click=lambda: st.session_state.update({"page": "doctor_dashboard"}))
    else:
        st.warning("Invalid user role. Please log in again.")
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
else:
    # --- User is not logged in ---
    st.sidebar.header("Login/Sign Up")
    login_or_signup = st.sidebar.radio("Choose an option:", ["Login", "Sign Up"])

    if login_or_signup == "Login":
        # --- Email Login ---
        st.sidebar.subheader("Login with Email")
        email = st.sidebar.text_input("Your Email", key="login_email")
        password = st.sidebar.text_input("Password", type="password", key="login_password")

        if st.sidebar.button("Login"):
            try:
                response = supabase.auth.sign_in_with_password(email=email, password=password)
                user = response.user
                user_role = user.user_metadata.get("role")
                st.success("Logged in successfully!")
                st.session_state["logged_in"] = True
                st.session_state["user_role"] = user_role
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error during login: {e}")

    else:
        # --- Email Sign Up ---
        st.sidebar.subheader("Sign Up with Email")
        new_email = st.sidebar.text_input("Your Email", key="signup_email")
        new_password = st.sidebar.text_input("Create Password", type="password", key="signup_password")
        chosen_role = st.sidebar.radio("Choose your role:", ["patient", "doctor"])

        if st.sidebar.button("Sign Up"):
            try:
                response = supabase.auth.sign_up(
                    email=new_email,
                    password=new_password,
                    user_metadata={"role": chosen_role}
                )
                st.success("Sign up successful! Please check your email for a confirmation link.")
            except Exception as e:
                st.error(f"Error during signup: {e}")

# --- Main Content (if not logged in) ---
if not st.session_state.get("logged_in", False):
    st.write("Learn more about the benefits of Ayurveda and how it can improve your well-being.")
    st.write("Ayurveda is an ancient holistic healing system that originated in India. It focuses on balancing the mind, body, and spirit to promote overall health and wellness.")
    st.write("Some key principles of Ayurveda include:")
    st.write("1. Personalized approach to health")
    st.write("2. Emphasis on prevention")
    st.write("3. Use of natural remedies and therapies")
    st.write("4. Mind-body connection")
    st.write("5. Balanced lifestyle")
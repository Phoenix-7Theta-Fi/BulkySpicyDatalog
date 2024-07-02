import streamlit as st
from supabase import create_client, Client

# --- Supabase Configuration ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Ayurvedic Healthcare", page_icon="🌿")

# --- Home Screen UI ---
st.title("Welcome to Our Ayurvedic Healthcare Platform")
st.write("Discover holistic wellness through the power of Ayurveda.")

# --- User Authentication and Role Management ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_role" not in st.session_state:
    st.session_state["user_role"] = None

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
        st.session_state["logged_in"] = False  # Log the user out if the role is invalid
        st.session_state["user_role"] = None
else:
    # --- User is not logged in ---
    st.sidebar.header("Login/Sign Up")
    login_or_signup = st.sidebar.radio("Choose an option:", ["Login", "Sign Up"])

    if login_or_signup == "Login":
        # --- Email Login ---
        st.sidebar.subheader("Login with Email")
        email = st.sidebar.text_input("Your Email")
        password = st.sidebar.text_password("Password")

        if st.sidebar.button("Login"):
            try:
                # Authenticate user with Supabase
                response = supabase.auth.sign_in_with_password(email=email, password=password)
                # Extract user data from response
                user = response.user
                # Assuming you have a 'role' attribute in the user metadata
                user_role = user.user_metadata.get("role")

                st.success("Logged in successfully!")
                st.session_state["logged_in"] = True
                st.session_state["user_role"] = user_role
            except Exception as e:
                st.error(f"Error during login: {e}")

    else:
        # --- Email Sign Up ---
        st.sidebar.subheader("Sign Up with Email")
        new_email = st.sidebar.text_input("Your Email")
        new_password = st.sidebar.text_password("Create Password")
        chosen_role = st.sidebar.radio("Choose your role:", ["patient", "doctor"])

        if st.sidebar.button("Sign Up"):
            try:
                # Create a new user in Supabase
                response = supabase.auth.sign_up(
                    email=new_email,
                    password=new_password,
                    user_metadata={"role": chosen_role}
                )

                # (Optional) Send a confirmation email (check Supabase docs)
                # supabase.auth.send_confirmation_email(email=new_email)

                st.success("Sign up successful! Please check your email for a confirmation link.")
            except Exception as e:
                st.error(f"Error during signup: {e}")

# --- Main Content (if not logged in) ---
if not st.session_state.get("logged_in", False):
    st.image("ayurveda_image.jpg", use_column_width=True)  # Replace with actual image path
    st.write(
        "Learn more about the benefits of Ayurveda and how it can improve your well-being."
    )
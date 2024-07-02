import streamlit as st
from ...utils import supabase  # Assuming you have the Supabase client in utils.py

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Doctor Dashboard", page_icon=":stethoscope:")

# --- Helper Functions ---
def get_doctor_name(user_id):
    """Fetches the doctor's name from the database."""
    # Replace with your actual table and column names
    doctor = (
        supabase.table("doctors").select("*").eq("user_id", user_id).single().execute().data
    )
    return doctor.get("name", "Dr. (Name not found)")  # Replace with your doctor's name column

def get_upcoming_appointments(doctor_id):
    """Fetches upcoming appointments for the doctor."""
    today = datetime.date.today()
    appointments = (
        supabase.table("appointments")
        .select("*")
        .eq("doctor_id", doctor_id)
        .gt("appointment_time", today) # Future appointments only
        .execute()
        .data
    )
    return appointments

# --- Dashboard UI ---
st.title("Welcome to Your Dashboard")

if st.session_state["logged_in"] and st.session_state["user_role"] == "doctor":
    user_id = st.session_state.get("user_id")
    doctor_name = get_doctor_name(user_id) 
    st.header(f"Welcome, {doctor_name}")

    # --- Upcoming Appointments ---
    st.subheader("Upcoming Appointments")
    doctor_id = st.session_state.get("doctor_id", None)  # You'll likely need to fetch this
    if doctor_id:
        appointments = get_upcoming_appointments(doctor_id) 
        if appointments:
            for appointment in appointments:
                # Format appointment time
                appointment_time = datetime.strptime(appointment['appointment_time'], "%Y-%m-%dT%H:%M:%S").strftime("%A, %B %d, %Y at %I:%M %p") 

                st.write(f"- **Patient:** {appointment.get('patient_id', 'N/A')} (ID: {appointment.get('id', 'N/A')})") # Replace with patient name if available 
                st.write(f"   - **Time:** {appointment_time}") 
                # ... Add more details like appointment status, links to consultation notes, etc.
        else:
            st.info("No upcoming appointments found.")
    else:
        st.warning("Unable to fetch appointments. Please make sure your profile is complete.")

    # --- Add other dashboard sections as needed --- 
    # - Recent patient messages
    # - Analytics or summaries (e.g., number of consultations this week/month)
    # - Quick links to other sections (Patient list, settings, etc.)

else:
    st.warning("You need to be logged in as a doctor to access this page.")
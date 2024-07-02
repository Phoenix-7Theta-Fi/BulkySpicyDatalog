import streamlit as st
from ...utils import supabase  # Import Supabase client
from datetime import datetime, timedelta

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Book a Consultation", page_icon=":calendar:"
)

# --- Helper Functions --- 
def fetch_doctors_from_supabase():
    """Fetches doctors data from your Supabase database."""
    # Replace with your actual table and column names
    doctors = supabase.table("doctors").select("*").execute().data
    return doctors


def create_appointment(doctor_id, appointment_time, patient_id):
    """Creates a new appointment in the database."""
    try:
        supabase.table("appointments").insert(
            {
                "doctor_id": doctor_id,
                "patient_id": patient_id, 
                "appointment_time": appointment_time,
                "status": "scheduled", # You can add other status like 'completed', 'cancelled'
            }
        ).execute()
        st.success("Appointment booked successfully!")
    except Exception as e:
        st.error(f"An error occurred while booking: {e}")

# --- Consultation Booking UI --- 
st.title("Book a Consultation with an Ayurvedic Practitioner")

# --- Fetch doctors from Supabase --- 
doctors = fetch_doctors_from_supabase()

# --- Doctor Selection ---
if doctors:
    doctor_options = {doctor.get('id'): doctor.get('name', 'No Name') for doctor in doctors}
    selected_doctor_id = st.selectbox("Choose a practitioner:", doctor_options.keys(), format_func=lambda x: doctor_options.get(x))

    if selected_doctor_id: 
        # --- Appointment Scheduling ---
        st.subheader("Schedule your consultation:")

        # Get the current date and time
        today = datetime.now()

        # Allow users to book within the next 7 days
        available_days = [today + timedelta(days=i) for i in range(7)]

        # Create a list of available time slots (adjust as needed)
        available_slots = [
            (today + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:00")
            for i in range(9, 17)  # Example: 9 AM to 5 PM
        ]

        selected_date = st.date_input(
            "Select a date:", value=today, min_value=today, max_value=available_days[-1]
        )
        selected_time = st.selectbox("Select a time slot:", available_slots)

        # Combine selected date and time
        selected_datetime_str = f"{selected_date.strftime('%Y-%m-%d')} {selected_time}"
        selected_appointment_time = datetime.strptime(selected_datetime_str, "%Y-%m-%d %H:%M:%S")

        if st.button("Book Appointment"):
            if st.session_state["logged_in"]:
                user_id = st.session_state.get("user_id")  # Assuming you store user_id in the session
                create_appointment(selected_doctor_id, selected_appointment_time, user_id)
            else:
                st.error("You need to log in to book an appointment.")

else:
    st.info("No doctors found in the database.") 
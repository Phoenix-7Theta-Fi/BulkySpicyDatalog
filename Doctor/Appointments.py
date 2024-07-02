import streamlit as st
from datetime import datetime, timedelta
from ...utils import supabase

# --- Streamlit Page Configuration --- 
st.set_page_config(page_title="Manage Appointments", page_icon=":calendar:")

# --- Helper Function ---
def get_doctor_appointments(doctor_id, date_filter=None):
    """Fetches appointments for the doctor, optionally filtered by date."""
    query = supabase.table("appointments").select("*").eq("doctor_id", doctor_id)

    if date_filter:
        if isinstance(date_filter, datetime): 
            # Filter by specific date 
            start_of_day = date_filter.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            query = query.gte("appointment_time", start_of_day).lt("appointment_time", end_of_day)
        elif isinstance(date_filter, str) and date_filter == "upcoming":
            # Filter for upcoming appointments (today and later)
            query = query.gte("appointment_time", datetime.now())

    appointments = query.execute().data
    return appointments

# --- Appointments UI --- 
st.title("Manage Your Appointments")

if st.session_state["logged_in"] and st.session_state["user_role"] == "doctor":
    doctor_id = st.session_state.get("doctor_id", None)

    if doctor_id:
        # --- Date Filtering ---
        st.sidebar.header("Filter Appointments")
        filter_option = st.sidebar.radio("Show:", ["All", "Upcoming", "By Date"]) 

        if filter_option == "By Date":
            selected_date = st.sidebar.date_input(
                "Select a Date:", value=datetime.today()
            )
            appointments = get_doctor_appointments(doctor_id, date_filter=selected_date) 
        elif filter_option == "Upcoming":
            appointments = get_doctor_appointments(doctor_id, date_filter="upcoming")
        else: 
            appointments = get_doctor_appointments(doctor_id)

        # --- Display Appointments ---
        if appointments:
            for appointment in appointments:
                appointment_time = datetime.strptime(appointment['appointment_time'], "%Y-%m-%dT%H:%M:%S").strftime("%A, %B %d, %Y at %I:%M %p")
                st.write(f"**Patient:** {appointment.get('patient_id', 'N/A')}") # Replace with patient name
                st.write(f"**Time:** {appointment_time}")
                st.write(f"**Status:** {appointment.get('status', 'N/A')}")
                # ... (Add buttons/links for actions - view details, start consultation, etc.) ... 
                st.write("---") 
        else:
            st.info("No appointments found for the selected criteria.") 

    else:
        st.warning("Unable to fetch appointments. Make sure your doctor ID is set correctly.")
else:
    st.warning("You need to be logged in as a doctor to view this page.")
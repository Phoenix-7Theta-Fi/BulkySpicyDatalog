import streamlit as st
import pandas as pd
from ...utils import supabase

# --- Streamlit Page Configuration --- 
st.set_page_config(page_title="Patient List", page_icon=":clipboard:")

# --- Helper Functions ---
def fetch_patients_for_doctor(doctor_id):
    """Fetches patients associated with the given doctor from Supabase."""
    # You might need a join or relationship between doctors, patients, and appointments
    # Here's a basic example assuming you have a 'doctor_id' in the 'patients' table 
    patients = (
        supabase.table("patients")
        .select("*")
        .eq("doctor_id", doctor_id) 
        .execute()
        .data
    )
    return patients

# --- Patient List UI ---
st.title("Your Patient List")

if st.session_state["logged_in"] and st.session_state["user_role"] == "doctor":
    doctor_id = st.session_state.get("doctor_id", None)  # You'll need to fetch/set this correctly

    if doctor_id:
        patients = fetch_patients_for_doctor(doctor_id)

        if patients:
            # Using st.data_editor for a more interactive table
            df_patients = pd.DataFrame(patients)

            # --- (Optional) Customizing Data Editor ---
            # Hide specific columns from the editor (e.g., patient ID)
            hide_columns = ['id', 'created_at'] # Replace with your column names
            column_config = {col: st.column_config.Column(hidden=True) for col in hide_columns if col in df_patients.columns}

            edited_df = st.data_editor(df_patients, num_rows="dynamic", column_config=column_config)

            # ... (Handle data updates if you want to allow edits) ...

        else:
            st.info("No patients found.") 
    else:
        st.warning("Unable to fetch patient list. Make sure your doctor ID is set correctly.")

else:
    st.warning("You need to be logged in as a doctor to view this page.")
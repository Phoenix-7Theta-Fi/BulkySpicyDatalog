import streamlit as st
import pandas as pd
import plotly.express as px  # For interactive charts
from ...utils import supabase # Assuming you have Supabase client in utils.py

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Your Health Analytics", page_icon=":chart_with_upwards_trend:"
)

# --- Helper Functions --- 
def fetch_patient_data(user_id):
    """Fetches all relevant patient data from Supabase."""
    # 1. Fetch AI Diagnosis History
    diagnosis_history = supabase.table("ai_diagnosis_history").select("*").eq("user_id", user_id).execute().data

    # 2. Fetch Product Usage Log 
    product_usage_log = supabase.table("product_usage_log").select("*").eq("user_id", user_id).execute().data

    # 3. Fetch Consultation Notes (You'll need to adjust based on how you store notes)
    consultation_notes = supabase.table("consultation_notes").select("*").eq("user_id", user_id).execute().data

    # ... Fetch any other relevant data for the patient ...

    return diagnosis_history, product_usage_log, consultation_notes 

# --- Health Analytics UI --- 
st.title("Your Health Analytics")

if st.session_state["logged_in"]:
    user_id = st.session_state.get("user_id") 

    # --- Fetch patient data ---
    diagnosis_history, product_usage_log, consultation_notes = fetch_patient_data(user_id)

    # --- AI Diagnosis History ---
    st.subheader("AI Diagnosis History")
    if diagnosis_history:
        for record in diagnosis_history:
            st.write(f"**Date:** {record.get('diagnosis_date', 'N/A')}") # Replace with your column name
            st.write(f"**Diagnosis:** {record.get('diagnosis', 'N/A')}") # Replace with your column name
            # ... Display other relevant fields from the diagnosis_history ... 
            st.write("---")
    else:
        st.info("No AI diagnosis history found.")

    # --- Product Usage Log --- 
    st.subheader("Product Usage Log")
    if product_usage_log: 
        # You can use st.dataframe or st.data_editor for better display of tabular data
        df_products = pd.DataFrame(product_usage_log)
        st.dataframe(df_products)
        # ... Customize product usage log display ...
    else: 
        st.info("No product usage log found.")

    # --- Consultation Notes ---
    st.subheader("Consultation Notes")
    if consultation_notes:
        for note in consultation_notes:
            st.write(f"**Date:** {note.get('consultation_date', 'N/A')}") # Replace with your column name
            st.write(f"**Notes:** {note.get('notes', 'N/A')}") # Replace with your column name
            st.write("---") 
    else:
        st.info("No consultation notes found.")

    # --- Add more analytics sections as needed ---
    # ...

else:
    st.warning("You need to be logged in to view your health analytics.")
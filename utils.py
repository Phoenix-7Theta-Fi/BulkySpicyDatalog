import streamlit as st
from supabase import create_client, Client
from vonage import Client as VonageClient 

# Load API keys and URLs securely using st.secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
VONAGE_API_KEY = st.secrets["VONAGE_API_KEY"]
VONAGE_API_SECRET = st.secrets["VONAGE_API_SECRET"]

# --- Initialize Supabase client ---
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Initialize Vonage Client (if you are using it) ---
vonage_client = VonageClient(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)

# (You can add more functions or initialization code for other APIs in this file)
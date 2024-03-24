import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file.
load_dotenv()

# Configuring the Google Generative AI with an API key from the environment.
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Access your GOOGLE_API_KEY
google_api_key = st.secrets["GOOGLE_API_KEY"]
import google.generativeai as genai
# from config import GOOGLE_API_KEY
import streamlit as st


# Access your GOOGLE_API_KEY
google_api_key = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=google_api_key)

# Access your GOOGLE_API_KEY
# google_api_key = st.secrets["GOOGLE_API_KEY"]

def get_gemini_response(question, context, age, retirement_age, risk_profile):
    full_context = f"{context} Age: {age}, Retirement Age: {retirement_age}, Risk Profile: {risk_profile}. {question}"
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(full_context)
    return response.text

import streamlit as st
import os
import re
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file.
load_dotenv()

# Configure the Google Generative AI with an API key from the environment.
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, context, age, retirement_age, risk_profile):
    # Include the additional user input in the context.
    full_context = f"{context} Age: {age}, Retirement Age: {retirement_age}, Risk Profile: {risk_profile}. {question}"
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(full_context)
    return response.text

# Function to parse LLM response and convert to a pandas DataFrame
def parse_llm_response_to_table(response):
    # Find all occurrences of patterns like "AAPL: 20%"
    matches = re.findall(r'(\w+):\s(\d+)%', response)
    # Create a DataFrame from the matches
    if matches:
        df_stocks = pd.DataFrame(matches, columns=["Stock", "Weight"])
        df_stocks["Weight"] = df_stocks["Weight"].astype(str) + "%"  # Add the percentage symbol
        return df_stocks
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no matches found

# Initialize the Streamlit app with a page configuration.
st.set_page_config(page_title="AI Driven Financial Advisor", layout="wide")

# UI Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');
    body {
        font-family: 'Montserrat', sans-serif;
        background-color: #F0F3F4;
    }
    .container {
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    h1, h2 {
        color: #2E86C1;
    }
    input, select, .stSlider {
        border: 1px solid #D0D3D4;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        width: 100%;
        box-sizing: border-box;
    }
    button {
        background-color: #2E86C1;
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    button:hover {
        background-color: #14659E; /* Slightly darker on hover */
    }
    </style>
    """, unsafe_allow_html=True)

# Set app title and description
st.markdown("<h1 style='color: #2E86C1;'>AI Driven Financial Advisor</h1>", unsafe_allow_html=True)
st.write("Welcome to your AI financial advisor. Please provide some details to get personalized financial advice.")

# Collect user inputs within a container for better layout management
with st.container():
    with st.form(key="user_info"):
        age = st.slider("Your Age:", min_value=18, max_value=100, value=30)
        retirement_age = st.slider("Your Desired Retirement Age:", min_value=18, max_value=100, value=60)
        risk_profile = st.selectbox("Your Risk Profile:", ["Low", "Medium", "High"])
        input_question = st.text_input("Your Financial Question:", key="input")
        submit_button = st.form_submit_button("Get Advice")

# If the "Get Advice" button is clicked, fetch and display the response.
if submit_button:
    context = "As a financial advisor, providing advice based on client's profile:"
    response = get_gemini_response(input_question, context, age, retirement_age, risk_profile)
    
    # Parsing the LLM response and creating a DataFrame for the stocks table
    df_recommended_stocks = parse_llm_response_to_table(response)
    
    # Creating a two-column layout
    col1, col2 = st.columns([1, 2])  # Adjust the ratio as needed

    with col1:
        st.markdown("<h2 style='color: #2E86C1;'>Recommended Portfolio</h2>", unsafe_allow_html=True)
        st.write(response)
    
    with col2:
        if not df_recommended_stocks.empty:
            st.markdown("<h2 style='color: #2E86C1;'>Recommended Asset Allocation</h2>", unsafe_allow_html=True)
            st.table(df_recommended_stocks)
        else:
            st.markdown("<h2 style='color: #2E86C1;'>No specific asset allocation could be derived from the response.</h2>", unsafe_allow_html=True)

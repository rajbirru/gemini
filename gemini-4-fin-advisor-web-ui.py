import streamlit as st
import os
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from dotenv import load_dotenv

# Load environment variables from .env file.
load_dotenv()

def to_markdown(text):
    text = text.replace('•', ' *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Configure the Google Generative AI with an API key from the environment.
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, context, age, retirement_age, risk_profile):
    # Include the additional user input in the context.
    full_context = f"{context} Age: {age}, Retirement Age: {retirement_age}, Risk Profile: {risk_profile}. {question}"
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(full_context)
    return response.text

# Initialize the Streamlit app with a page configuration.
st.set_page_config(page_title="Financial Advisor Q&A", layout="centered")

# **UI Styling**
st.markdown(
    """
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

    input, select { 
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
    """,
    unsafe_allow_html=True,
)

# Set color scheme
primary_color = "#2E86C1"
secondary_color = "#EAECEE"

# Set app title and description
st.markdown(f"<h1 style='color: {primary_color};'>AI Driven Financial Advisor</h1>", unsafe_allow_html=True)
st.write("Welcome to your AI financial advisor. Please provide some details to get personalized financial advice.")

# Collect user inputs within a container for better layout management
with st.container():
    with st.form(key="user_info"):
        age = st.slider("Your Age:", min_value=18, max_value=100, value=30)
        retirement_age = st.slider("Your Desired Retirement Age:", min_value=18, max_value=100, value=60)
        risk_profile = st.selectbox("Your Risk Profile:", ["Low", "Medium", "High"])
        input_question = st.text_input("Your Financial Question:", key="input")
        submit = st.form_submit_button("Get Advice")

# If the "Get Advice" button is clicked, fetch and display the response.
if submit:
    # Prepare a generic context for financial advice.
    context = "As a financial advisor, providing advice based on client's profile:"
    response = get_gemini_response(input_question, context, age, retirement_age, risk_profile)
    st.markdown(f"<h2 style='color: {primary_color};'>Recommendd Portfolio</h2>", unsafe_allow_html=True)
    st.write(response)

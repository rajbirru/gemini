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
  text = text.replace('•', '  *')
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
st.set_page_config(page_title="Financial Advisor Q&A")

st.header("Financial Advice Application")

st.write("Welcome to your digital financial advisor. Please provide some details to get personalized financial advice.")

# Collect user inputs.
age = st.number_input("Your Age:", min_value=18, max_value=100, value=30, step=1)
retirement_age = st.number_input("Your Desired Retirement Age:", min_value=18, max_value=100, value=60, step=1)
risk_profile = st.selectbox("Your Risk Profile:", ["Low", "Medium", "High"])

input_question = st.text_input("Your Financial Question:", key="input")

submit = st.button("Get Advice")

# If the "Get Advice" button is clicked, fetch and display the response.
if submit:
    # Prepare a generic context for financial advice.
    context = "As a financial advisor, providing advice based on client's profile:"
    response = get_gemini_response(input_question, context, age, retirement_age, risk_profile)
    st.subheader("Advice")
    st.write(response)

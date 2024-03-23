import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import openai
import os

# Load the OpenAI API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

def fetch_etf_recommendations(risk_profile, age, retirement_age):
    # Constructing the prompt for the LLM
    prompt = f"Given a {risk_profile} risk profile, age {age}, and retirement age {retirement_age}, suggest 10 ETFs."
    response = openai.Completion.create(
      engine="davinci",  # You may choose a different engine based on your needs
      prompt=prompt,
      temperature=0.7,
      max_tokens=100,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    etfs = response.choices[0].text.strip().split('\n')
    return etfs

# Streamlit app setup
st.set_page_config(page_title="ETF Advisor")
st.header("ETF Advisor")

# User inputs
risk_profile = st.selectbox("Select your risk profile:", ["Low", "Medium", "High"], key="risk_profile")
age = st.number_input("What is your age?", min_value=18, max_value=100, step=1, key="age")
retirement_age = st.number_input("At what age do you plan to retire?", min_value=age, max_value=100, step=1, key="retirement_age")

# Button to get ETF recommendations
if st.button("Get ETF Recommendations"):
    etfs = fetch_etf_recommendations(risk_profile, age, retirement_age)
    st.write("Recommended ETFs based on your input:")
    st.write(etfs)

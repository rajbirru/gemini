import streamlit as st
from model import get_gemini_response
from styles import load_styles  # Ensure this is imported if you're using a separate styles.py


def extract_recommended_stocks(response):
    # Initialize an empty list to store the recommended stocks
    recommended_stocks = []
    
    # Split the response into lines
    lines = response.split("\n")
    
    # Iterate over each line in the response
    for line in lines:
        # Check if the line contains the keyword "Recommended Stocks"
        if "Recommended Stocks" in line:
            # Extract the part of the line after the keyword
            stocks_string = line.split("Recommended Stocks:")[-1].strip()
            
            # Split the stocks string by commas and remove any leading/trailing whitespace
            stocks = [stock.strip() for stock in stocks_string.split(",")]
            
            # Append the recommended stocks to the list
            recommended_stocks.extend(stocks)
    
    return recommended_stocks

# Must be the first command in your app
st.set_page_config(page_title="AI Driven Financial Advisor", layout="wide")

# Load and inject CSS styles
st.markdown(load_styles(), unsafe_allow_html=True)

# Set app title and description
st.markdown("<h1 style='color: #2E86C1;'>AI Driven Financial Advisor</h1>", unsafe_allow_html=True)
st.write("Welcome to your AI financial advisor. Please provide some details to get personalized financial advice.")

# Define session state for the responses and context if not already defined
if 'response' not in st.session_state:
    st.session_state['response'] = ""
if 'context' not in st.session_state:
    st.session_state['context'] = "As a financial advisor, providing advice based on client's profile:"
if 'recommended_stocks' not in st.session_state:
    st.session_state['recommended_stocks'] = []

# Collect user inputs within a container for better layout management
with st.container():
    age = st.slider("Your Age:", min_value=18, max_value=100, value=30)
    retirement_age = st.slider("Your Desired Retirement Age:", min_value=18, max_value=100, value=60)
    risk_profile = st.selectbox("Your Risk Profile:", ["Low", "Medium", "High"])
    input_question = st.text_input("Your Financial Question:", key="input")
    submit_button = st.button("Get Advice")

# Handle the response from the initial advice request
if submit_button:
    with st.spinner("Generating advice..."):
        try:
            st.session_state['response'] = get_gemini_response(input_question, st.session_state['context'], age, retirement_age, risk_profile)
            
            # Extract recommended stocks from the response and store them in the session state
            st.session_state['recommended_stocks'] = extract_recommended_stocks(st.session_state['response'])
        except Exception as e:
            st.error(f"An error occurred while generating advice: {str(e)}")

# Display the initial advice
if st.session_state['response']:
    st.markdown("<h2 style='color: #2E86C1;'>Recommended Portfolio</h2>", unsafe_allow_html=True)
    st.write(st.session_state['response'])
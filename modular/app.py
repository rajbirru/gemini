import streamlit as st
from gtts import gTTS
from io import BytesIO
import pandas as pd
from model import get_gemini_response
from styles import load_styles
from utils import extract_recommended_stocks
from context import get_system_context
from prompt_templates import get_response_template
from portfolio_analysis import run_portfolio_analysis
from visualizations import create_gradient_bar
import re
# import pyttsx3

# # Initialize the text-to-speech engine globally
# engine = pyttsx3.init()

# Must be the first command in your app
st.set_page_config(page_title="AI Driven Financial Advisor", layout="wide")

# Load and inject CSS styles
st.markdown(load_styles(), unsafe_allow_html=True)

# Set app title
st.markdown("<h1 style='color: #2E86C1;'>AI Driven Financial Advisor</h1>", unsafe_allow_html=True)

def read_text(text):
    tts = gTTS(text, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp, format='audio/mp3')

# Define session state for the responses and context if not already defined
if 'response' not in st.session_state:
    st.session_state['response'] = ""
if 'context' not in st.session_state:
    st.session_state['context'] = get_system_context()
if 'recommended_stocks' not in st.session_state:
    st.session_state['recommended_stocks'] = []

# User input section
with st.container():
    st.write("Welcome to your AI financial advisor. Please provide some details to get personalized financial advice.")
    st.write("")
    age = st.slider("Your Age:", min_value=18, max_value=100, value=30)
    st.write("")
    retirement_age = st.slider("Your Desired Retirement Age:", min_value=18, max_value=100, value=60)
    st.write("")
    risk_profile = st.selectbox("Your Risk Profile:", ["Low", "Medium", "High"])
    st.write("")
    input_question = st.text_input("Your Financial Question:", key="input")
    submit_button = st.button("Get Advice", key="advice_button", help="Click to generate personalized financial advice")

# Handle the response from the initial advice request
if submit_button:
    with st.spinner("Generating advice..."):
        try:
            # Construct the detailed prompt using the provided arguments
            detailed_prompt = (
                f"{get_system_context()}\n{get_response_template()}\n"
                f"Given a {age}-year-old individual aiming for retirement by age {retirement_age} "
                f"with a {risk_profile.lower()} risk profile, "
                f"{input_question}\n"
                "Considering current market conditions, suggest a diversified portfolio of 10 to 20 stocks and ETFs. "
                "Provide a brief rationale for each recommendation."
            )

            # Print the constructed prompt for debugging purposes
            print("Constructed Prompt:")
            print(detailed_prompt)

            # Call get_gemini_response with the constructed detailed prompt and other required arguments
            st.session_state['response'] = get_gemini_response(input_question, detailed_prompt, age, retirement_age, risk_profile)
            st.session_state['recommended_stocks'] = extract_recommended_stocks(st.session_state['response'])

        except Exception as e:
            st.error(f"An error occurred while generating advice: {str(e)}")

# Display the initial advice
if st.session_state['response']:
    st.markdown("<h2 style='color: #2E86C1;'>Recommended Portfolio</h2>", unsafe_allow_html=True)
    st.write(st.session_state['response'])
    read_text(st.session_state['response'])  # Read the explanation

# Display the stock/bond split as a gradient bar
if st.session_state['response']:
    stock_match = re.search(r'Stocks: (\d+(?:\.\d+)?)%', st.session_state['response'])
    bond_match = re.search(r'Bonds: (\d+(?:\.\d+)?)%', st.session_state['response'])
    
    if stock_match and bond_match:
        stock_percentage = float(stock_match.group(1))
        bond_percentage = float(bond_match.group(1))
        gradient_bar = create_gradient_bar(stock_percentage, bond_percentage)
        
        st.markdown(
            f'<div style="background-image: linear-gradient(to right, green {stock_percentage}%, red {bond_percentage}%); '
            f'height: 20px; width: 100%; border-radius: 10px; margin-bottom: 20px;"></div>',
            unsafe_allow_html=True
        )

# Extract and display the portfolio allocation table
table_match = re.search(r'Portfolio Allocation:\n(.*?)\n\n', st.session_state['response'], re.DOTALL)
if table_match:
    table_data = table_match.group(1)
    table_rows = [row.split('|')[1:-1] for row in table_data.strip().split('\n')]
    
    styled_table = f'<table style="width: 100%; border-collapse: collapse;">'
    for row in table_rows:
        styled_table += f'<tr style="background-color: #f2f2f2;">'
        for cell in row:
            styled_table += f'<td style="padding: 8px; text-align: center; border: 1px solid #ddd;">{cell.strip()}</td>'
        styled_table += '</tr>'
    styled_table += '</table>'
    st.markdown(styled_table, unsafe_allow_html=True)

# Portfolio analysis section
# Enable this section if you want to include portfolio analysis directly in app.py, ensuring you have the necessary logic in place
# Make sure to handle the file object directly without assuming it's saved on disk
# st.markdown("<h2 style='color: #2E86C1;'>Portfolio Analysis</h2>", unsafe_allow_html=True)
run_portfolio_analysis(st.session_state['response'])

# Remember to pass the engine as an argument to functions needing text-to-speech capabilities

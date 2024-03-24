# Streamlit framework and auxiliary tools
import streamlit as st
from gtts import gTTS
from io import BytesIO

# Data manipulation and analysis tools
import pandas as pd

# Modularization of functionality across the app
from model import get_gemini_response
from styles import load_styles
from utils import extract_recommended_stocks
from context import get_system_context
from prompt_templates import get_response_template
from portfolio_analysis import run_portfolio_analysis
from visualizations import create_gradient_bar

# Standard library imports
import re

# Set Streamlit page configuration as the first action
st.set_page_config(page_title="AI Driven Financial Advisor", layout="wide")

# Inject custom CSS styles
st.markdown(load_styles(), unsafe_allow_html=True)

# Set app title with HTML for styling
st.markdown("<h1 style='color: #2E86C1;'>AI Driven Financial Advisor</h1>", unsafe_allow_html=True)

def read_text(text):
    tts = gTTS(text, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp.read(), format='audio/mp3')  # Ensure you're passing the bytes to st.audio

# Initialize session state variables if they are not already defined
default_values = {"response": "", "context": get_system_context(), "recommended_stocks": []}
for key, default_value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# User inputs through the Streamlit UI
with st.container():
    st.write("Welcome to your AI financial advisor. Please provide some details to get personalized financial advice.")
    
    # Collecting user inputs
    age = st.slider("Your Age:", min_value=18, max_value=100, value=30)
    retirement_age = st.slider("Your Desired Retirement Age:", min_value=18, max_value=100, value=60)
    risk_profile = st.selectbox("Your Risk Profile:", ["Low", "Medium", "High"])
    input_question = st.text_input("Your Financial Question:", key="input")
    
    # Submission button to trigger advice generation
    submit_button = st.button("Get Advice", key="advice_button", help="Click to generate personalized financial advice")

# Process user request and generate advice upon form submission
if submit_button:
    with st.spinner("Generating advice..."):
        try:
            # Constructing a detailed prompt for the model
            detailed_prompt = f"{get_system_context()}\n{get_response_template()}\n" \
                              f"Given a {age}-year-old aiming for retirement by age {retirement_age} " \
                              f"with a {risk_profile.lower()} risk profile, {input_question}\n" \
                              "Considering current market conditions, suggest a diversified portfolio."

            # Call model to get advice based on the user's inputs
            response = get_gemini_response(input_question, detailed_prompt, age, retirement_age, risk_profile)
            st.session_state['response'] = response
            st.session_state['recommended_stocks'] = extract_recommended_stocks(response)

        except Exception as e:
            # Display any errors encountered during the model call
            st.error(f"An error occurred while generating advice: {str(e)}")


# Display the generated advice and read it out using text-to-speech
if st.session_state['response']:
    st.markdown("<h2 style='color: #2E86C1;'>Recommended Portfolio</h2>", unsafe_allow_html=True)
    st.write(st.session_state['response'])
    read_text(st.session_state['response'])  # Text-to-speech for the advice


# Visualize the stock/bond split using a gradient bar
if 'response' in st.session_state and st.session_state['response']:
    stock_match = re.search(r'Stocks: (\d+(?:\.\d+)?)%', st.session_state['response'])
    bond_match = re.search(r'Bonds: (\d+(?:\.\d+)?)%', st.session_state['response'])
    if stock_match and bond_match:
        stock_percentage = float(stock_match.group(1))
        bond_percentage = float(bond_match.group(1))
        st.markdown(create_gradient_bar(stock_percentage, bond_percentage), unsafe_allow_html=True)

# Extract and display the portfolio allocation table from the response
table_match = re.search(r'Portfolio Allocation:\n(.*?)\n\n', st.session_state['response'], re.DOTALL)
if table_match:
    # Parsing the table data
    table_data = table_match.group(1)
    table_rows = [row.split('|')[1:-1] for row in table_data.strip().split('\n')]

    # Assuming you know the column names, or they can be dynamically determined
    column_names = ["Column 1", "Column 2", "Column 3"]  # Adjust this based on your actual data

    # Create a DataFrame from your list of lists
    df = pd.DataFrame(table_rows, columns=column_names)

    # Choose one method to display the table based on your needs:
    st.dataframe(df)  # For an interactive table
    # OR
    # st.table(df)  # For a static table

# Portfolio analysis section
# Enable this section if you want to include portfolio analysis directly in app.py, ensuring you have the necessary logic in place
# Make sure to handle the file object directly without assuming it's saved on disk
# st.markdown("<h2 style='color: #2E86C1;'>Portfolio Analysis</h2>", unsafe_allow_html=True)
run_portfolio_analysis(st.session_state['response'])

# Remember to pass the engine as an argument to functions needing text-to-speech capabilities
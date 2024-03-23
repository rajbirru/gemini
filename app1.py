import streamlit as st
from model import get_gemini_response
from utils import parse_llm_response_to_table
from styles import load_styles

# Must be the first command in your app
st.set_page_config(page_title="AI Driven Financial Advisor", layout="wide")

# Load and inject CSS styles
st.markdown(load_styles(), unsafe_allow_html=True)

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
    
    # Parse the LLM response and create a DataFrame for the stocks table
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
            # No allocation was derived from the initial response, provide user feedback option
            if st.button("Request Detailed Asset Allocation"):
                follow_up_question = "Can you provide a specific asset allocation for the recommended portfolio?"
                detailed_response = get_gemini_response(follow_up_question, context, age, retirement_age, risk_profile)
                df_recommended_stocks = parse_llm_response_to_table(detailed_response)
                
                if not df_recommended_stocks.empty:
                    st.markdown("<h2 style='color: #2E86C1;'>Detailed Asset Allocation</h2>", unsafe_allow_html=True)
                    st.table(df_recommended_stocks)
                else:
                    st.markdown("<h2 style='color: #2E86C1;'>No specific asset allocation could be derived from the responses.</h2>", unsafe_allow_html=True)
import streamlit as st

def get_user_inputs():
    """
    Generates UI elements for capturing user inputs and returns the values.
    
    Returns:
        age (int): The user's current age.
        retirement_age (int): The age at which the user wishes to retire.
        risk_profile (str): The user's risk tolerance level.
        financial_question (str): The user's financial query.
    """
    st.subheader("Welcome to your AI financial advisor. Please provide some details to get personalized financial advice.")

    # Age Slider
    age = st.slider("Your Age:", min_value=18, max_value=100, value=30, help="Select your current age.")
    
    # Retirement Age Slider
    retirement_age = st.slider("Your Desired Retirement Age:", min_value=age, max_value=100, value=60, help="Select the age at which you aim to retire.")
    
    # Risk Profile Select Box
    risk_profile = st.selectbox("Your Risk Profile:", ["Low", "Medium", "High"], help="Choose your investment risk tolerance level.")
    
    # Financial Question Text Input
    financial_question = st.text_input("Your Financial Question:", help="Type your financial query or goal here.")
    
    return age, retirement_age, risk_profile, financial_question

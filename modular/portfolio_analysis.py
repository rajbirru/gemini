import streamlit as st
import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI  # Make sure to update to langchain-openai as suggested if applicable
from langchain_openai import OpenAI

import pyttsx3

# Initialize the LLM
llm = OpenAI(temperature=0.7)

# This function is no longer needed to be defined here if it's used from app.py

def analyze_portfolio(engine, portfolio_file, recommended_portfolio):
    try:
        # Directly read the uploaded file without saving to disk
        portfolio_df = pd.read_csv(portfolio_file)

        # Calculate the total portfolio value
        portfolio_value = portfolio_df['Value'].sum()

        # Calculate the weights of stocks and bonds in the uploaded portfolio
        portfolio_stock_weight = portfolio_df[portfolio_df['Type'] == 'Stock']['Value'].sum() / portfolio_value * 100
        portfolio_bond_weight = portfolio_df[portfolio_df['Type'] == 'Bond']['Value'].sum() / portfolio_value * 100

        # Extract the recommended stock and bond percentages from the recommended portfolio
        recommended_stock_weight = float(recommended_portfolio.split('Stocks: ')[1].split('%')[0])
        recommended_bond_weight = float(recommended_portfolio.split('Bonds: ')[1].split('%')[0])

        # Display the portfolio summary
        st.write("Portfolio Summary:")
        st.write(f"Total Portfolio Value: ${portfolio_value:.2f}")
        st.write(f"Stock Weight: {portfolio_stock_weight:.2f}%")
        st.write(f"Bond Weight: {portfolio_bond_weight:.2f}%")

        st.markdown("<h3 style='color: #2E86C1;'>Target Portfolio:</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight: bold; font-size: 16px;'>Recommended Stock Weight: {recommended_stock_weight:.2f}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight: bold; font-size: 16px;'>Recommended Bond Weight: {recommended_bond_weight:.2f}%</p>", unsafe_allow_html=True)

        # Provide advice on adjusting the stock allocation
        advice = "Your portfolio is aligned with the recommended portfolio."
        if portfolio_stock_weight < recommended_stock_weight:
            advice = "Consider increasing your allocation to stocks to align with the recommended portfolio."
        elif portfolio_stock_weight > recommended_stock_weight:
            advice = "Consider decreasing your allocation to stocks to align with the recommended portfolio."
        
        st.markdown(f"<p style='font-weight: bold; font-size: 18px;'>{advice}</p>", unsafe_allow_html=True)
        read_text(engine, advice)  # Pass the engine object to the function for text-to-speech

    except Exception as e:
        st.error(f"Error analyzing portfolio: {str(e)}")

def read_text(engine, text):
    engine.say(text)
    engine.runAndWait()

def run_portfolio_analysis(engine, recommended_portfolio):
    st.markdown("<h2 style='color: #2E86C1;'>Portfolio Analysis</h2>", unsafe_allow_html=True)
    # File uploader for the portfolio
    portfolio_file = st.file_uploader("Upload your portfolio (CSV file)", type="csv")
    if portfolio_file is not None:
        analyze_portfolio(engine, portfolio_file, recommended_portfolio)

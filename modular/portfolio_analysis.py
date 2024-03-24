import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
# Ensure you import the necessary modules for your LLM operations
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# Assuming langchain_openai is correctly set up and replaces langchain_community.llms
from langchain_openai import OpenAI

# Initialize the LLM
llm = OpenAI(temperature=0.7)

def analyze_portfolio(portfolio_file, recommended_portfolio):
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
        read_text(advice)  # Using gTTS for text-to-speech

    except Exception as e:
        st.error(f"Error analyzing portfolio: {str(e)}")

def read_text(text):
    tts = gTTS(text, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp, format='audio/mp3')

def run_portfolio_analysis(recommended_portfolio):
    st.markdown("<h2 style='color: #2E86C1;'>Portfolio Analysis</h2>", unsafe_allow_html=True)
    # File uploader for the portfolio
    portfolio_file = st.file_uploader("Upload your portfolio (CSV file)", type="csv")
    if portfolio_file is not None:
        analyze_portfolio(portfolio_file, recommended_portfolio)

import streamlit as st
import pandas as pd
from langchain import PromptTemplate, LLMChain, OpenAI
import pyttsx3
import os

# Initialize the LLM
llm = OpenAI(temperature=0.7)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def read_text(text):
    # Stop the engine if it's running
    if engine._inLoop:
        engine.endLoop()

    engine.say(text)
    engine.startLoop()

# Define the prompt template
advice_prompt_template = PromptTemplate(
    input_variables=["portfolio_stock_weight", "recommended_stock_weight"],
    template="""
Given the following information:
Portfolio Stock Weight: {portfolio_stock_weight}%
Recommended Stock Weight: {recommended_stock_weight}%

Provide a detailed explanation for the advice on adjusting the stock allocation to align with the recommended portfolio.
""",
)

# Create the LLM chain
advice_chain = LLMChain(llm=llm, prompt=advice_prompt_template)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def analyze_portfolio(portfolio_file, recommended_portfolio):
    try:
        # Read the uploaded portfolio file
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

        st.markdown(f"<h3 style='color: #2E86C1;'>Target Portfolio:</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight: bold; font-size: 16px;'>Recommended Stock Weight: {recommended_stock_weight:.2f}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight: bold; font-size: 16px;'>Recommended Bond Weight: {recommended_bond_weight:.2f}%</p>", unsafe_allow_html=True)

        # Provide advice on adjusting the stock allocation
        if portfolio_stock_weight < recommended_stock_weight:
            advice = "Consider increasing your allocation to stocks to align with the recommended portfolio."
            advice_explanation = advice_chain.run(portfolio_stock_weight=portfolio_stock_weight, recommended_stock_weight=recommended_stock_weight)
            st.markdown(f"<p style='font-weight: bold; font-size: 18px;'>{advice}</p>", unsafe_allow_html=True)
            st.write(advice_explanation)
            read_advice(advice)
        elif portfolio_stock_weight > recommended_stock_weight:
            advice = "Consider decreasing your allocation to stocks to align with the recommended portfolio."
            advice_explanation = advice_chain.run(portfolio_stock_weight=portfolio_stock_weight, recommended_stock_weight=recommended_stock_weight)
            st.markdown(f"<p style='font-weight: bold; font-size: 18px;'>{advice}</p>", unsafe_allow_html=True)
            st.write(advice_explanation)
            read_advice(advice)
        else:
            advice = "Your stock allocation aligns with the recommended portfolio."
            st.markdown(f"<p style='font-weight: bold; font-size: 18px;'>{advice}</p>", unsafe_allow_html=True)
            read_advice(advice)

    except Exception as e:
        st.error(f"Error analyzing portfolio: {str(e)}")

def read_advice(advice):
    engine.say(advice)
    engine.runAndWait()

def run_portfolio_analysis(recommended_portfolio):
    st.markdown("<h2 style='color: #2E86C1;'>Portfolio Analysis</h2>", unsafe_allow_html=True)
    # File uploader for the portfolio
    portfolio_file = st.file_uploader("Upload your portfolio (CSV file)", type="csv")
    if portfolio_file is not None:
        # Get the absolute path of the uploaded file
        portfolio_file_path = os.path.join(os.getcwd(), portfolio_file.name)
        analyze_portfolio(portfolio_file_path, recommended_portfolio)
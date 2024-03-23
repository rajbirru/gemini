import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
# import openai  # Uncomment and configure if you're using OpenAI's GPT-3.

def fetch_etf_recommendations(risk_profile, age, retirement_age):
    # Placeholder for LLM ETF recommendation logic.
    # Replace this with a call to your LLM, e.g., GPT-3 asking for ETF recommendations.
    # Example using GPT-3:
    # response = openai.Completion.create(
    #   engine="text-davinci-003",
    #   prompt=f"Given a {risk_profile} risk profile, age {age}, and retirement age {retirement_age}, suggest 10 ETFs.",
    #   temperature=0.7,
    #   max_tokens=150,
    #   top_p=1.0,
    #   frequency_penalty=0.0,
    #   presence_penalty=0.0
    # )
    # return parse_response_to_list(response)  # Implement parsing based on your response structure.
    # This is a dummy list for demonstration purposes:
    return ['SPY', 'VOO', 'VTI', 'QQQ', 'ARKK', 'IVV', 'IWM', 'EFA', 'VXX', 'XLF']

def fetch_latest_prices(etfs):
    prices = {}
    for etf in etfs:
        data = yf.Ticker(etf)
        prices[etf] = data.history(period="1d")["Close"][-1]
    return prices

# Initialize Streamlit application.
st.set_page_config(page_title="ETF Advisor")
st.header("ETF Advisor")

# User inputs.
risk_profile = st.selectbox("Select your risk profile:", ["Low", "Medium", "High"], key="risk_profile")
age = st.number_input("What is your age?", min_value=18, max_value=100, step=1, key="age")
retirement_age = st.number_input("At what age do you plan to retire?", min_value=age, max_value=100, step=1, key="retirement_age")

# Button to generate ETF recommendations.
if st.button("Get ETF Recommendations"):
    etfs = fetch_etf_recommendations(risk_profile, age, retirement_age)
    prices = fetch_latest_prices(etfs)
    
    # Display ETFs and their latest prices in a table.
    df = pd.DataFrame(list(prices.items()), columns=['ETF', 'Latest Price'])
    st.table(df)
    
    # Dropdown to select an ETF to plot.
    selected_etf = st.selectbox("Select an ETF to generate a chart:", etfs, key="selected_etf")
    
    if st.button("Generate Chart"):
        data = yf.download(selected_etf, period="1y")
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], label='Close Price')
        plt.title(f"{selected_etf} Close Price (Past Year)")
        plt.xlabel("Date")
        plt.ylabel("Close Price (USD)")
        plt.legend()
        st.pyplot(plt)

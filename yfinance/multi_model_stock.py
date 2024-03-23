import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)

# Initialize your Streamlit application
st.set_page_config(page_title="Stock/ETF Graph Generator")
st.header("Stock/ETF Graph Generator")

# Input for the stock symbol
stock_symbol = st.text_input("Enter the stock symbol (e.g., AAPL, TSLA, etc.):", key="stock_symbol")

# Date input for the start and end date
start_date = st.date_input("Start date", key="start_date")
end_date = st.date_input("End date", key="end_date")

# Button to generate the plot
if st.button("Generate Graph"):
    if stock_symbol:
        # Fetch historical data from Yahoo Finance
        data = yf.download(stock_symbol, start=start_date, end=end_date)
        
        # Check if data is empty
        if data.size == 0:
            st.write("No data found for the given symbol and date range. Please try again.")
        else:
            # Plotting the 'Close' price data
            plt.figure(figsize=(10, 5))
            plt.plot(data.index, data['Close'], label='Close Price')
            plt.title(f"{stock_symbol} Close Price")
            plt.xlabel("Date")
            plt.ylabel("Close Price (USD)")
            plt.legend()
            
            # Display the plot in Streamlit
            st.pyplot(plt)
    else:
        st.write("Please enter a stock symbol.")

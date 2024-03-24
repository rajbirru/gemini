# market_summary.py

import google.generativeai as genai

def configure_genai(api_key):
    genai.configure(api_key=api_key)

# Function to get a general market summary
def get_market_summary():
    context = (
        "Provide a summary of today's market trends including key economic indicators "
        "such as the S&P 500, DOW, NASDAQ, unemployment rates, Federal Funds Rate, "
        "inflation, and other relevant gauges."
    )
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(context)
    return response.text

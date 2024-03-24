import re
import pandas as pd

def parse_llm_response_to_table(response):
    matches = re.findall(r'(\w+):\s(\d+)%', response)
    if matches:
        df_stocks = pd.DataFrame(matches, columns=["Stock", "Weight"])
        df_stocks["Weight"] = df_stocks["Weight"].astype(str) + "%"
        return df_stocks
    else:
        return pd.DataFrame()

def extract_recommended_stocks(response):
    # Initialize an empty list to store the recommended stocks
    recommended_stocks = []
    # Split the response into lines
    lines = response.split("\n")
    # Iterate over each line in the response
    for line in lines:
        # Check if the line contains the keyword "Recommended Stocks"
        if "Recommended Stocks" in line:
            # Extract the part of the line after the keyword
            stocks_string = line.split("Recommended Stocks:")[-1].strip()
            # Split the stocks string by commas and remove any leading/trailing whitespace
            stocks = [stock.strip() for stock in stocks_string.split(",")]
            # Append the recommended stocks to the list
            recommended_stocks.extend(stocks)
    return recommended_stocks
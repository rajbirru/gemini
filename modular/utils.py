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

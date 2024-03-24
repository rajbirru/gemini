import pandas as pd
import streamlit as st
from gtts import gTTS
from io import BytesIO

def analyze_portfolio(portfolio_file, recommended_portfolio):
    try:
        portfolio_df = pd.read_csv(portfolio_file)
        portfolio_value = portfolio_df['Value'].sum()
        portfolio_stock_weight = portfolio_df[portfolio_df['Type'] == 'Stock']['Value'].sum() / portfolio_value * 100
        portfolio_bond_weight = portfolio_df[portfolio_df['Type'] == 'Bond']['Value'].sum() / portfolio_value * 100
        recommended_stock_weight = float(recommended_portfolio.split('Stocks: ')[1].split('%')[0])
        recommended_bond_weight = float(recommended_portfolio.split('Bonds: ')[1].split('%')[0])

        st.write("Portfolio Summary:")
        st.write(f"Total Portfolio Value: ${portfolio_value:.2f}")
        st.write(f"Stock Weight: {portfolio_stock_weight:.2f}%")
        st.write(f"Bond Weight: {portfolio_bond_weight:.2f}%")

        st.markdown("<h3 style='color: #2E86C1;'>Target Portfolio:</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight: bold; font-size: 16px;'>Recommended Stock Weight: {recommended_stock_weight:.2f}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight: bold; font-size: 16px;'>Recommended Bond Weight: {recommended_bond_weight:.2f}%</p>", unsafe_allow_html=True)

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

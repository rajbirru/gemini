# summarize_text.py
import openai
import re
import streamlit as st

def clean_text(text):
    """
    Cleans the text by removing or replacing unwanted characters and formatting.

    Parameters:
    - text (str): The text to clean.

    Returns:
    - str: The cleaned text.
    """
    # Replace dashes with spaces. Adjust the pattern as needed.
    text = re.sub(r'-+', ' ', text)
    # Remove special characters, keeping only letters, numbers, and spaces. Adjust as needed.
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Replace newline characters with spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def summarize_text(text, openai_api_key):
    """
    Summarizes the given text using an LLM via the OpenAI API after cleaning it.

    Parameters:
    - text (str): The text to be summarized.
    - openai_api_key (str): Your OpenAI API key.

    Returns:
    - str: The summarized text.
    """
    # Load the OpenAI API key from the environment variable
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    openai.api_key = openai_api_key

    text = clean_text(text)  # Clean the text first

    response = openai.Completion.create(
      engine="text-davinci-003",  # Or whichever engine you prefer
      prompt=f"Summarize this for a general audience in a natural and engaging manner:\n{text}",
      temperature=0.7,
      max_tokens=150,  # Adjust based on your needs
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    return response.choices[0].text.strip()

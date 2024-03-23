import streamlit as st
import os
import fitz  # PyMuPDF
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def pdf_to_text(pdf_path):
    """Extracts text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def get_gemini_summary(text):
    """Assuming a generic function to get summary from Gemini API. Adjust based on actual capabilities."""
    model = genai.GenerativeModel('gemini-pro')  # Use an appropriate model or method for summarization
    response = model.generate_content(text)  # This would be a summarization call, adjust accordingly
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="PDF Summarizer")
st.header("PDF Summarizer Application")

pdf_file = st.file_uploader("Upload a PDF to summarize:", type=["pdf"], key="pdf_file")

if st.button("Summarize"):
    if pdf_file:
        text = pdf_to_text(pdf_file)
        summary = get_gemini_summary(text)  # You may need to handle larger texts in chunks
        st.subheader("Summary")
        st.write(summary)
    else:
        st.write("Please upload a PDF file.")

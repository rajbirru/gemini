import streamlit as st
import os
import base64
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def image_to_base64(image):
    """Converts an image to base64 string."""
    return base64.b64encode(image.getvalue()).decode()

def get_gemini_response(text, image=None):
    model = genai.GenerativeModel('gemini-pro-vision')  # Assuming 'gemini-pro-vision' for multimodal.
    parts = [text]
    if image:
        base64_image = image_to_base64(image)
        # Assuming the API expects an image in base64 in this format, adjust based on actual API documentation
        parts.append({'mime_type': 'image/jpeg', 'data': base64_image})
    
    response = model.generate_content(parts)  # Adjust this part based on the actual method signature for images
    return response.text

# Initialize our Streamlit app
st.set_page_config(page_title="Multimodal Q&A Demo")
st.header("Gemini Multimodal Application")

text_input = st.text_input("Enter your question here:", key="text_input")
image_input = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"], key="image_input")

submit = st.button("Ask")

if submit:
    response = get_gemini_response(text_input, image_input)
    st.subheader("The Response is")
    st.write(response)

import streamlit as st
import os
import base64
import google.generativeai as genai
from dotenv import load_dotenv
from io import BytesIO
from google.api_core.exceptions import GoogleAPIError

load_dotenv()  # take environment variables from .env.

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def image_to_base64(image):
    """Converts an image to base64 string."""
    return base64.b64encode(image.getvalue()).decode()

def base64_to_image(base64_str):
    """Converts a base64 string back to an image."""
    return BytesIO(base64.b64decode(base64_str))

def get_gemini_response(text, image=None):
    model_name = 'gemini-pro-vision'  # Updated to the model that supports images
    try:
        model = genai.GenerativeModel(model_name)
        parts = [text]
        if image:
            base64_image = image_to_base64(image)
            parts.append({'mime_type': 'image/jpeg', 'data': base64_image})
        
        response = model.generate_content(parts)
        # Assuming the response structure includes attributes 'text' and 'image_data'
        # Adjust the following line if the structure is different
        return response.text if not image else base64_to_image(response.image_data)
    except GoogleAPIError as e:
        st.error(f"Failed to get response: {e}")
        return None


# Initialize our Streamlit app
st.set_page_config(page_title="Multimodal Q&A Demo")
st.header("Gemini Multimodal Application")

text_input = st.text_input("Enter your text here:", key="text_input")
image_input = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"], key="image_input")

submit = st.button("Submit")

if submit and text_input:
    response = get_gemini_response(text_input, image_input)
    if response:
        st.subheader("The Response is")
        if isinstance(response, BytesIO):
            st.image(response, caption='Generated Image')
        else:
            st.write(response)

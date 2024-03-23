import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(question, context, age, retirement_age, risk_profile):
    full_context = f"{context} Age: {age}, Retirement Age: {retirement_age}, Risk Profile: {risk_profile}. {question}"
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(full_context)
    return response.text

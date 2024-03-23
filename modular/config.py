import os
from dotenv import load_dotenv

# Load environment variables from .env file.
load_dotenv()

# Configuring the Google Generative AI with an API key from the environment.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

import os
from google import genai# — Google API client —
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print(GOOGLE_API_KEY)
client = genai.Client(api_key=GOOGLE_API_KEY)
# The Gemini model we'll use for scoring
MODEL_NAME = "gemini-2.0-flash"

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

NUM_PROFILES = 2
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
OUTPUT_CSV = Path("langchain_structured_profiles.csv")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

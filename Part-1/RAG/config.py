import os
from dotenv import load_dotenv

load_dotenv()

# — Hugging Face model ID
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "unsloth/llama-3.2-3b-instruct")

# — File paths (edit these!)
PROFILES_CSV   = "data\langchain_structured_profiles.csv"  # your profiles

QUESTIONS_TXT  = "data\questions.txt"                     # one question per line
OUTPUT_CSV     = "RAG\output\personalized_answers.csv"        # results out

NGROK_URL = 'https://59b2-34-125-19-158.ngrok-free.app'

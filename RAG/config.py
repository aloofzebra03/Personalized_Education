import os
from dotenv import load_dotenv

load_dotenv()

# — Hugging Face model ID
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "unsloth/llama-3.2-3b-instruct")

# — File paths (edit these!)
PROFILES_CSV   = "RAG\data\langchain_structured_profiles.csv"  # your profiles

QUESTIONS_TXT  = "RAG\data\questions.txt"                     # one question per line
OUTPUT_CSV     = "RAG\output\personalized_answers.csv"        # results out

NGROK_URL = 'https://1cdb-35-237-161-146.ngrok-free.app'

import os
from dotenv import load_dotenv

load_dotenv()

# — Hugging Face model ID
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "aloofzebra03/Llama_50_profiles")

# — File paths (edit these!)
PROFILES_CSV   = r"data\langchain_structured_profiles.csv"  # your profiles

QUESTIONS_TXT  = r"data\questions.txt"                     # one question per line
OUTPUT_CSV     = r"Finetuned_Answers\output\finetune_personalized_answers.csv"        # results out

NGROK_URL = 'https://327b-34-143-134-2.ngrok-free.app'

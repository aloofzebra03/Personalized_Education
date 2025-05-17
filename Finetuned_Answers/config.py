import os
from dotenv import load_dotenv

load_dotenv()

# — Hugging Face model ID
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "unsloth/llama-3.2-3b-instruct")

# — File paths (edit these!)
PROFILES_CSV   = r"Finetuned_Answers\data\langchain_structured_profiles.csv"  # your profiles

QUESTIONS_TXT  = r"Finetuned_Answers\data\questions.txt"                     # one question per line
OUTPUT_CSV     = r"Finetuned_Answers\output\finetune_personalized_answers.csv"        # results out

NGROK_URL = 'https://b1ce-34-127-2-120.ngrok-free.app'

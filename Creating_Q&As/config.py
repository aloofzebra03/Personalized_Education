from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
# MODEL_NAME = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
# MODEL_NAME = 'google/flan-t5-base'
# MODEL_NAME = 'google/gemma-2-2b-it'
# MODEL_NAME = 'HuggingFaceH4/zephyr-7b-beta'
MODEL_NAME = 'gemini-1.5-flash'

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

PROFILE_CSV_PATH = r"Personalized_Education/Creating_Q&As/data/student_profiles.csv"
QUESTION_LIST_PATH = r"Personalized_Education/Creating_Q&As/data/questions.txt"

OUTPUT_JSONL_PATH = r"Personalized_Education\Creating_Q&As\output\generated_qas.jsonl"
OUTPUT_CSV_PATH = r"Personalized_Education\Creating_Q&As\output\generated_qas.csv"
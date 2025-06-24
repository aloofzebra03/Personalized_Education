from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

NUM_PROFILES = 50
# MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
# MODEL_NAME = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
# MODEL_NAME = 'google/flan-t5-base'
# MODEL_NAME = 'google/gemma-2-2b-it'
# MODEL_NAME = 'HuggingFaceH4/zephyr-7b-beta'
MODEL_NAME = 'gemini-2.0-flash'

OUTPUT_CSV = Path("Creating_Student_Params/output/langchain_student_params_50_streamlit_testing.csv")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

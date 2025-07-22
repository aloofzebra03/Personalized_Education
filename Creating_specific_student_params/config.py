from pathlib import Path
import os
import streamlit as st

GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY_1")

NUM_PROFILES = 50
# MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
# MODEL_NAME = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
# MODEL_NAME = 'google/flan-t5-base'
# MODEL_NAME = 'google/gemma-2-2b-it'
# MODEL_NAME = 'HuggingFaceH4/zephyr-7b-beta'
MODEL_NAME = 'gemini-2.0-flash'

OUTPUT_CSV = Path("Creating_Student_Params_From_Json/output/student_params_from_json.csv")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME     = "gemini-2.0-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

STUDENT_PARAMS_CSV = "Creating_Section_Params/data/langchain_student_params_1500_reduced.csv"
SECTION_PARAMS_CSV = "Creating_Section_Params/data/next_section_ranges_chatgpt.csv.csv"
OUTPUT_CSV = "Creating_Section_Params/output/ground_truth_sections_params_temp0.csv"

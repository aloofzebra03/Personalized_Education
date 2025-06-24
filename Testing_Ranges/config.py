import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
STUDENT_PARAMS_CSV = "data/langchain_student_params_1500_reduced.csv"
OUTPUT_CSV         = "Testing_Ranges/output/next_section_ground_truth.csv"

# LLM Settings
MODEL_NAME     = "gemini-2.0-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Next sections list
NEXT_SECTIONS = [
    "Concept Definition",
    "Explanation (with analogies)",
    "Details (facts, sub-concepts)",
    "Intuition",
    "Logical Flow",
    "Working",
    "Critical Thinking",
    "MCQs",
    "Real-Life Application",
    "What-if Scenarios"
]

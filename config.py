from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

NUM_PROFILES = 2
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"
OUTPUT_CSV = Path("langchain_structured_profiles.csv")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

INSTRUCTION_TEMPLATE = '''
You are a school counselor. Generate a synthetic student profile for class {class_level}.
All fields must be logically consistent, realistic, and match the schema exactly. 
Output ONLY the raw JSON object and ensure values follow these rules:

- Age between 13–17, class between 8–11.
- Include interests, hobbies, 2 personality traits.
- Marks must be 60–100.
- Use syllabi from CBSE, ICSE, IB, IGCSE.
- Include rich, personal stories and digital/home context.

Strictly follow the JSON schema fields and types.
'''

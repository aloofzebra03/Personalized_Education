
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME     = "gemini-1.5-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

HF_API_KEY          = os.getenv("HF_API_KEY", "")
# HF_EMBEDDING_MODEL  = "sentence-transformers/all-mpnet-base-v2"
HF_EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

# Chroma
CHROMA_PERSIST_DIR = "Creating_section_text/chroma_db"

# PDF to ingest
PDF_PATH = r"Creating_Section_Text/data/Chapter8.pdf"

TEST_PARAMS_PATH = "Creating_Section_Text/test/params.json"

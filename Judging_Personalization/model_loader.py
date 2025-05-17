# models/llm_loader.py
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY

def get_judge_llm(model_name: str = "models/gemini-pro", temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=GOOGLE_API_KEY
    )

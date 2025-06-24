# model_loader.py

from langchain_google_genai import ChatGoogleGenerativeAI
from Creating_Section_Params.config import MODEL_NAME, GOOGLE_API_KEY

def get_llm():
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        api_key=GOOGLE_API_KEY,
        temperature=0.5,
        max_new_tokens=100000,
        transport="rest"
    )

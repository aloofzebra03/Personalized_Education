from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL_NAME, GOOGLE_API_KEY

def load_llm():
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        api_key=GOOGLE_API_KEY,
        temperature=0.0,
        top_p=1.0,
        max_output_tokens=2048,
        transport="rest"           # ← add this!

    )

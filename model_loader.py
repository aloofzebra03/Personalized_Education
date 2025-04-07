from langchain_community.llms import HuggingFaceEndpoint
from config import HF_API_TOKEN, MODEL_NAME

from langchain_huggingface import HuggingFaceEndpoint
from config import MODEL_NAME, HF_API_TOKEN

def load_llm():
    return HuggingFaceEndpoint(
        repo_id=MODEL_NAME,
        huggingfacehub_api_token=HF_API_TOKEN,
        temperature=0.7,
        max_new_tokens=512
    )


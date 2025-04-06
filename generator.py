from .model_loader import load_llm
from .prompt_builder import prompt, parser

llm = load_llm()
chain = prompt | llm | parser

def generate_profile(class_level: int):
    return chain.invoke({"class_level": str(class_level)})

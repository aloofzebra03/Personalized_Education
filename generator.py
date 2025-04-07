from model_loader import load_llm
from prompt_builder import prompt, parser
from schema import StudentProfile

llm = load_llm()
chain = prompt | llm | parser

def generate_profile():
    return chain.invoke({})
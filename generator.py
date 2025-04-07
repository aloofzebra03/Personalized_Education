from model_loader import load_llm
from prompt_builder import prompt, parser

llm = load_llm()
chain = prompt | llm | parser

def generate_profile(class_level: int):
    return chain.invoke({"class_level": str(class_level)})

# from model_loader import load_llm
# from schema import StudentProfile
# from config import INSTRUCTION_TEMPLATE

# def generate_profile(class_level: int):
#     structured_llm = load_llm().with_structured_output(StudentProfile)
#     instruction = INSTRUCTION_TEMPLATE.format(class_level=class_level)
#     return structured_llm.invoke({"input": instruction})

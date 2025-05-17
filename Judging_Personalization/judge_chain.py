# chains/judge_chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from schema import PersonalizationEvaluation
from langchain_google_genai import ChatGoogleGenerativeAI

def build_judge_chain(llm: ChatGoogleGenerativeAI):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert evaluator. Your task is to assess how well a tutor's answer is personalized to a student profile.\n\n"
                   "Personalization includes:\n"
                   "- Using the student's interests\n"
                   "- Adapting to strengths, weaknesses, or preferred learning style\n"
                   "- Avoiding irrelevant or invented personal information\n\n"
                   "Respond in JSON format with a 'score' (1 to 5) and 'explanation'."),
        ("human", "Student Profile:\n{student_profile}\n\nQuestion:\n{question}\n\nTutor Answer:\n{tutor_answer}")
    ])
    parser = PydanticOutputParser(pydantic_object=PersonalizationEvaluation)
    return prompt | llm | parser

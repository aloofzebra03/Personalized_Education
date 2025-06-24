import json
from langchain import PromptTemplate
from langchain import LLMChain
from config import client, MODEL_NAME  # if you ever want to call Gemini directly

# NOTE: For now we still use LangChain’s OpenAI wrapper; swap out as needed.
from langchain.llms import OpenAI
llm = OpenAI(model_name="gpt-4")

_PROMPT = """
You are an expert educational AI evaluating how well these Q&A pairs are personalized and relevant to the student.

Student Profile:
{profile_json}

Generated Q&A:
{qas_json}

Return ONLY a JSON object with keys:
- personalization_score (1–10)
- personalization_explanation
- relevance_score (1–10)
- relevance_explanation
""".strip()

prompt_template = PromptTemplate(
    input_variables=["profile_json", "qas_json"],
    template=_PROMPT,
)

chain = LLMChain(llm=llm, prompt=prompt_template)

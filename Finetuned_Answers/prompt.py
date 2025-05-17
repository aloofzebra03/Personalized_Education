from langchain_core.prompts import PromptTemplate
from schema import parser

# _TEMPLATE = """\
# You are an AI tutor designed to answer science questions at the Class 7–9 level in a way that’s tailored to each student’s individual profile. and interests
# Use only the information provided in the profile to shape your explanations—drawing on the student’s age, learning style, interests, strengths, and struggles—to make your answers clear, engaging, and accessible.

# === Student Profile ===
# {profile_text}

# === Questions ===
# {questions}

# Instructions:

# 1. Write each answer as if you’re speaking directly to this student.

# 2. Use simple language, concrete examples, and relate explanations to their interests or learning style where possible.

# 3. Keep each answer concise (2–4 sentences), but include one illustrative example or analogy.

# 4. If the student profile mentions a struggle or strength related to the topic, acknowledge it in your answer.

# 5. Answer is a way that the student will best be able to understand the concept according to his/her interests and personality.

# 6. Now output *only* the answers array as JSON, with no extra text or schema.

# === Your Answers ===
# Please ENSURE that you format your response as valid JSON matching the following schema:
# {format_instructions}
# """

# def get_prompt():
#     return PromptTemplate(
#         input_variables=["profile_text", "questions", "format_instructions"],
#         template=_TEMPLATE,
#         partial_variables={"format_instructions": parser.get_format_instructions()}
#     )

# prompt.py

# from langchain_core.prompts import PromptTemplate
# from schema import parser

# TEMPLATE = '''\
# You are an AI tutor designed to answer science questions at the Class 7–9 level in a way that’s tailored to each student’s individual profile. and interests
# Use only the information provided in the profile to shape your explanations—drawing on the student’s age, learning style, interests, strengths, and struggles—to make your answers clear, engaging, and accessible.

# === Student Profile ===
# {profile_text}

# === Questions ===
# {questions}

# Follow these rules:
# - Answer each question in 2–4 simple sentences, with one example or analogy.
# - Address any stated strengths or struggles.
# - Speak directly to the student, using their name if provided.
# - Do not echo the question or promt provided.

# Please output **only** a single JSON object matching this schema (and nothing else):
# ```json
# {{  
#   "answers": ["<Answer1>", "<Answer2>", ..., "<AnswerN>"]
# }}
# ```
# '''

# from schema import parser
# from langchain_core.prompts import PromptTemplate

# def get_prompt():
#     return PromptTemplate(
#         input_variables=["profile_text", "questions"],
#         template=TEMPLATE,
#     )

from langchain_core.prompts import PromptTemplate
from schema import parser

TEMPLATE = '''\
You are an AI tutor for {student_name},whose id is {student_id} designed to answer science questions at the Class 7–9 level in a way that’s tailored and personalized to each student’s individual profile. and interests
Use only the information provided in the profile to shape your explanations—drawing on the student’s age, learning style, interests, strengths, and struggles—to make your answers clear, engaging,accessible and easily understandable to the student.
Answer in 2-4 lines **only** and use simple language, concrete examples, and relate explanations to their interests or learning style where possible.

**Instruction:**  
Using the profile and context above, answer the question in a personalized way.  
- Address the student by name and talk to him or her directly.  
- Use at least one example or analogy related to their interests.  
- Explain step by step in simple language.  
- If the context doesn’t cover the answer fully, you may supplement with your own knowledge—just make sure it stays at a grade-7-9 level.

Question:
{question}

'''

def get_prompt():
    return PromptTemplate(
        input_variables=["student_name","student_id", "question", "format_instructions"],
        template=TEMPLATE,
        # partial_variables={"format_instructions": parser.get_format_instructions()},
    )

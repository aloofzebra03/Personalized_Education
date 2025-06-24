import json
from typing import List
# from langchain.output_parsers import OutputParserException
from langchain.prompts.base import BasePromptTemplate

def personalize_question(question: str, student_id: int) -> str:
    return question.replace("the student", "student with ID {student_id}").replace("The student", "student with ID {student_id}")

def batch_questions(questions: List[str], batch_size: int = 10) -> List[List[str]]:
    return [questions[i:i + batch_size] for i in range(0, len(questions), batch_size)]

def generate_qas(profile_row: dict, question_batches: List[List[str]], prompt: BasePromptTemplate, model, parser) -> List[dict]:

    student_id = profile_row.get("student_id", "unknown_student")
    profile_str = json.dumps(profile_row, indent=2)
    qa_pairs = []

    for batch in question_batches:
        personalized_batch = [personalize_question(q, student_id) for q in batch]
        question_block = "\n".join(f"{i+1}. {q}" for i, q in enumerate(personalized_batch))

        output = prompt | model | parser
        parsed_result = output.invoke({
            "profile": profile_str,
            "questions": question_block
        })

        for qa in parsed_result.root:
            qa_pairs.append({
                "student_id": student_id,
                "question": qa.question,
                "answer": qa.answer
            })
    return qa_pairs

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from prompts.schema import QABatch

def build_prompt_and_parser():
    parser = PydanticOutputParser(pydantic_object=QABatch)

    prompt = PromptTemplate(
        input_variables=["profile", "questions"],
        template="""
        You are a helpful AI tutor that takes student profiles and answers questions about them in a given format.
        Here is a student profile:
        {profile}
        Here are 10 questions about the student:
        {questions}
        Please return a list of 10 JSON objects like:
        [
          {{ "question": "...", "answer": "..." }},
          ...
        ]
        Instructions:
        - Start directly with the JSON object list. Do not add any other text or explanation.
        - All fields are filled logically with the help of the given profile only.
        - All values must be realistic and consistent.
        - Output MUST be valid JSON (no Markdown, no formatting).
        - Do **not** wrap the output in triple backticks or markdown.
        - Do **not** add an extra closing `}}`.
        - Do **not** escape underscores — use plain field names like `class_level`, not `class\\_level`.
        - Start each JSON object with `{{` and end with `}}`.

        START WITH THE JSON OBJECT DIRECTLY AND DO NOT ADD ANY OTHER TEXT OR EXPLANATION.

        Only use information present in the profile. NEVER make up anything on qour own.
        {format_instructions}
        """,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    return prompt, parser

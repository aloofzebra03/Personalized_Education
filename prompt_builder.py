

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from schema import StudentProfile

parser = PydanticOutputParser(pydantic_object=StudentProfile)

# prompt = PromptTemplate(
#     template = """You are a school counselor. Generate 1 synthetic student profiles such that each profile includes all the following fields.

# Instructions:
# - Don't echo the prompt in your output anywhere ever.
# - You DIRECTLY start with the json objects without any additional text or explanation in the beginning.
# - All fields are filled logically and do not conflict with each other.
# - The output is strictly in **standard JSON format** only.
# - Output **only** the JSON object — no additional explanations, markdown, or comments at the start end or middle.
# - Each student profile must be separated using the delimiter: ---END_OF_PROFILE---
# - Start each JSON object with `{{` and end with `}}`.
# - Do **not** wrap the output in triple backticks or markdown.
# - Do **not** add an extra closing `}}`.
# - Do **not** escape underscores — use plain field names like `class_level`, not `class\\_level`.
# - All values must be realistic and consistent.

# Below is the required format of the profile you must generate:
# {format_instructions}

# IMPORTANT: DO NOT REPEAT any of the profiles already generated below. Make the new profiles DISTINCT to the ones already existing.

# Previously generated profiles:
# {memory_block}"""
# ,
#     input_variables=["memory_block"],
#     partial_variables={"format_instructions": parser.get_format_instructions()}
# )

# Instructions:
# - Start directly with the JSON array of student profiles. Do not add any other text or explanation.
# - All fields are filled logically and do not conflict with each other.
# - The output is strictly in **standard JSON format** only.
# - Output **only** the JSON object — no additional explanations, markdown, or comments at the start end or middle.
# - Start each JSON object with `{{` and end with `}}`.
# - Do **not** wrap the output in triple backticks or markdown.
# - Do **not** add an extra closing `}}`.
# - Do **not** escape underscores — use plain field names like `class_level`, not `class\\_level`.
# - All values must be realistic and consistent.
# - DO NOT REPEAT any student from the list of previously generated profiles given  below.
# - All fields must be logically consistent, realistic, and diverse.
# - Output MUST be valid JSON (no Markdown, no formatting).

prompt = PromptTemplate(
    template = """<s>[INST] You are a school counselor and a json object producer that knows how to give output in standard json formar only. Your job is to generate 1 synthetic student profile.
    I want to take your standard json output and directly pass it to a pydantic output parser without any
    further processing or cleaning.There should NOT be any lists or arrays around it.
     So please make sure that you follow the schema that I have provided and DO NOT add any extra text or explanation in the beginning or end of the output.

I want to generate multiple distinct profie so I am giving you a list of previously generated profiles as well.Ensure that
the profiles you generate are not the same as the ones listed below. The names and other fields like
Intersts,Personality,Hobbies Learning Style,Pattern of Learning etc should be completely different but still FOLLOW the schema provided.
Previously generated profiles:
{memory_block}

Only use the following field names and types. DO NOT repeat this block in your output. Only use it as a reference:
{format_instructions}

Respond with a JSON object containing 1 diverse student profile. Your output should look like:

  {{ "name": "Example1", ... }}

Instructions:
- Start directly with the JSON object of student profiles. Do not add any other text or explanation.
- All fields are filled logically and do not conflict with each other.
- All values must be realistic and consistent.
- DO NOT REPEAT any student from the list of previously generated profiles given  below.
- All fields must be logically consistent, realistic, and diverse.
- Output MUST be valid JSON (no Markdown, no formatting).
- Do **not** wrap the output in triple backticks or markdown.
- Do **not** add an extra closing `}}`.
- Do **not** escape underscores — use plain field names like `class_level`, not `class\\_level`.
- Start each JSON object with `{{` and end with `}}`.
START WITH THE JSON OBJECT DIRECTLY AND DO NOT ADD ANY OTHER TEXT OR EXPLANATION.
[/INST]
""",
    input_variables=["memory_block"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)


__all__ = ["prompt", "parser"]

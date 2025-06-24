import json
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from schema2 import NextSectionRange, StudentParameters
from config import NEXT_SECTIONS

# 1️⃣ Build a parser expecting MANY NextSectionRange objects
parser = PydanticOutputParser(pydantic_object=NextSectionRange, many=True)
format_instructions = parser.get_format_instructions()

# 2️⃣ Prompt template (with placeholders)
template = """
You are an AI tutor designing an adaptive‐learning sequence.
You have these student parameters (JSON schema):
{student_schema}

You may choose ONE of these next sections for each distinct range:
{sections_list}

TASK:
For each section, output an object with:
- section_name
- numeric fields → <field>_min and <field>_max
- categorical fields → repeat the same value in both min/max
- list field content_type_preference → list of allowed types
- ongoing_concept may cover multiple concept names if desired.You may also decide that the ongoing_concept does not affect the next section prediction, in which case you can put all possible concepts in the each list.

Ensure that the ranges for different sections do not overlap.So that they can be used to differentiate the next section for different students.
This data will be used to generate ground truths for making a tree based model for next section prediction.
Make sure that the ranges are such that for different student parameters they give different next sections.It shouldn't be that the range for a particular section is so big that it can fit all students in it.
Return your answer STRICTLY as a JSON **array** matching this schema:
{format_instructions}
""".strip()

range_prompt = PromptTemplate(
    input_variables=["student_schema", "sections_list"],
    partial_variables={"format_instructions": format_instructions},
    template=template
)

def build_inputs():
    # Use the JSON schema of StudentParameters to describe the fields
    student_schema = json.dumps(
        StudentParameters.model_json_schema()['properties'], indent=2
    )
    sections_list = json.dumps(NEXT_SECTIONS, indent=2)
    return {
        "student_schema": student_schema,
        "sections_list": sections_list
    }, parser, range_prompt

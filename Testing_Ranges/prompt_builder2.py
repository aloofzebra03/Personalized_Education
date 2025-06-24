# prompt_builder2.py

import json
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from schema2 import NextSectionRange, StudentParameters
from config import NEXT_SECTIONS

# 1️⃣ Build a parser expecting ONE NextSectionRange object per call
parser = PydanticOutputParser(pydantic_object=NextSectionRange, many=False)
format_instructions = parser.get_format_instructions()

# 2️⃣ Prompt template for one section at a time
template = """
You are an AI tutor designing an adaptive‐learning sequence.

STUDENT PARAMETERS (JSON schema):
{student_schema}

COMPLETE LIST OF SECTIONS that need ranges generated for for you reference to plan the ranges accordingly:
{sections_list}

TARGET SECTION for this call:
{section_name}

PREVIOUSLY GENERATED RANGES (must be disjoint):
{prev_ranges}

TASK:
Generate exactly one object with:
- section_name
- for each numeric field: <field>_min and <field>_max
- for each categorical field: repeat the same value in both min/max
- content_type_preference: list of allowed content types
- Remember that you are generating for only a particular section right now but eventually have to generate ranges for all sections.And the ranges have to be from withing the ranges given in the current schema so plan accordingly

Ensure the new range does NOT overlap any in PREVIOUSLY GENERATED RANGES.
Return your answer STRICTLY as a JSON **object** matching this schema:
{format_instructions}
""".strip()

range_prompt = PromptTemplate(
    input_variables=["student_schema", "section_name", "prev_ranges"],
    partial_variables={"format_instructions": format_instructions},
    template=template
)

def build_inputs():
    student_schema = json.dumps(
        StudentParameters.model_json_schema()["properties"], indent=2
    )
    sections_list = json.dumps(NEXT_SECTIONS, indent=2)
    return {
        "student_schema": student_schema,
        "sections_list": sections_list
    }, parser, range_prompt

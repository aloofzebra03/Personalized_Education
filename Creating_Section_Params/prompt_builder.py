# prompt_builder.py

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from Creating_Section_Params.schema import NextSectionChoice

# Build parser and format instructions
output_parser       = PydanticOutputParser(pydantic_object=NextSectionChoice)
format_instructions = output_parser.get_format_instructions()

# Static list of sections
SECTIONS = [
    "Concept Definition",
    "Explanation (with analogies)",
    "Details (facts, sub-concepts)",
    "Intuition",
    "Logical Flow",
    "Working",
    "Critical Thinking",
    "MCQs",
    "Real-Life Application",
    "What-if Scenarios",
]

# Prompt: clearly state to choose the best section for the student’s current params
prompt = PromptTemplate(
    input_variables=[
        "student_json",
        "student_schema_json",
        "sections",
    ],
    partial_variables={
        "format_instructions": format_instructions
    },
    template="""
You are an AI tutor planning “Measurement of Time and Motion” content. Your job is to choose the best next section for a student based on their current parameters.

Your task is to analyze the student's current profile and parameter ranges, then select the most appropriate section from the provided list for the student to do next with the goal of increasing the student's understanding of the ongoing concept. Also, you have to assign each section parameter an integer from 1–5 based on the current student parameters.

1. STUDENT PROFILE (current values):

{student_json}
2. STUDENT PARAMETER SCHEMA WITH RANGES (for you to understand where values of the current student stand with respect to the schema):

{student_schema_json}

3. ONGOING CONCEPT:
The field ongoing_concept specifies the concept that the student is currently learning. It is a string that represents the name of the concept.

4. AVAILABLE SECTIONS (choose exactly one section from the below that would be best for the student given their current parameters):

{sections}

5. YOUR TASK:

Analyze the student's current parameters from the student_json in context of the max and min possible values from the schema.
Assign each section parameter an integer from 1–5 based on the current student parameters with the goal of ensuring the student understands the ongoing concept thoroughly.
Then, choose the best section from the available sections that would be most beneficial for the student to learn next, considering their current understanding and the ongoing concept.
Note: The sections that you need to choose from are the ones listed in the sections. You must choose one of these sections as the next section for the student. DO NOT confuse these with the student parameters. They are completely different. The knowledge_graph_nodes_covered in the student parameters schema are the concepts that the student has learned till now. Your goal is to suggest the next section that would be best for the student given their current parameters, including the concepts covered and the ongoing concept.

{format_instructions}
""".strip()
)

# prompt_code.py
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from schema import StudentParameters

# Initialize a parser based on our Pydantic schema
parser = PydanticOutputParser(pydantic_object=StudentParameters)

# Define the prompt template
prompt = PromptTemplate(
    template="""<s>[INST] You are a synthetic student profile generator that creates one JSON object conforming exactly to the `StudentParameters` schema.

Memory Block (previous profiles):
{memory_block}

Requirements:
1. Output must be a single JSON object (no arrays or extra lists) starting with `{{` and ending with `}}`.
2. Fill all fields per the schema, using realistic, consistent values; do not add extra properties.
3. Ensure the new profile does NOT duplicate any in the memory block above.
4. Field values must make logical sense together (e.g., high `test_anxiety_level` with low `conceptual_clarity_level`).
5. If unable to generate a unique profile after 3 tries, output exactly:
   {{{{"error": "Unable to generate unique profile after 3 attempts."}}}}
6. Do NOT include any explanatory text, Markdown, or backticks—only the raw JSON object.

Schema reference (for LLM; not to be output):
{format_instructions}

# Begin generation:
""",
    input_variables=["memory_block"],  # memory_block is injected here
    partial_variables={"format_instructions": parser.get_format_instructions()                       }
)

__all__ = ["prompt", "parser"]

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from schema import StudentParameters

# Initialize a parser based on our Pydantic schema
parser = PydanticOutputParser(pydantic_object=StudentParameters)

# Define the new prompt template
prompt = PromptTemplate(
    template="""
<s>[INST] You are a student-parameter generator.  
You will be given a JSON object with detailed information about a single student;  
use it to produce exactly one JSON object conforming to the `StudentParameters` schema.

Student Details JSON:
{student_json}

Requirements:
1. Output must be a single JSON object (no arrays/lists), starting with `{{` and ending with `}}`.
2. Fill **all** fields from the schema, no extra properties.
3. Field values must be internally consistent (e.g., high anxiety with low clarity).
4. If you cannot map the input JSON to a valid profile, output exactly:
   `{{"error": "Unable to generate profile from provided JSON."}}`
5. Do **not** include any markdown, explanatory text, or backticks—only raw JSON.

Schema reference (for LLM; not to be output):
{format_instructions}

# Begin generation:
""",
    input_variables=["student_json"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

__all__ = ["prompt", "parser"]

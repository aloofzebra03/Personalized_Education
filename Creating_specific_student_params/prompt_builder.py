from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from Creating_specific_student_params.schema import StudentParameters

# Initialize a parser based on our Pydantic schema
parser = PydanticOutputParser(pydantic_object=StudentParameters)

# Define the new prompt template
prompt = PromptTemplate(
    template="""
<s>[INST] You are a student-parameter generator.  
You will be given a JSON object with detailed responses of a single student on a particular topic. You are given the questions asked and the responses the student gave along with reasoning.
You also have the score that the child received on the reasoning,the time taken by the student to answer the entire questionnaire and the help the student received.
Use it to produce exactly one JSON object conforming to the `StudentParameters` schema. Make sure you judge the student comprehensively based on the responses and the score given to them.
Fill the roll_no column with the given roll number of the student here `{roll_no}`.
Student Details JSON:
{student_json}

Requirements:
1. Output must be a single JSON object (no arrays/lists), starting with `{{` and ending with `}}`.
2. Fill **all** fields from the schema, no extra properties.
3. Field values must be internally consistent (e.g., high anxiety with low clarity).
4. If you cannot map the input JSON to a valid profile, output exactly:
   `{{"error": "Unable to generate profile from provided JSON."}}`
5. Do **not** include any markdown, explanatory text, or backticks—only raw JSON.

**Note on Scores**  
• All score fields (answerScore, reasoningScore, totalScore, overallScore) are in "obtained/max" format.  
• Use the numerator for actual performance and the denominator for context (difficulty, consistency, etc.)  
• Infer schema fields (clarity, retention, error patterns, etc.) accordingly.

Schema reference (for LLM; not to be output):
{format_instructions}

# Begin generation:
""",
    input_variables=["student_json","roll_no"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

__all__ = ["prompt", "parser"]

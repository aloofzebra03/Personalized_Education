from Creating_Student_Params_From_Json.model_loader import load_llm
from Creating_Student_Params_From_Json.prompt_builder import prompt, parser
from Creating_Student_Params_From_Json.schema import StudentParameters
import re, json

llm = load_llm()
chain = prompt | llm

def extract_and_parse(raw: str):
    # Clean up markdown/backticks/BOM
    text = raw.lstrip('\ufeff').strip().strip('`')
    # Grab JSON object
    match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in response")
    blob = match.group(1)
    blob = blob.replace('\\n', '').replace('\\"', '"').replace("\\'", "'")
    data = json.loads(blob)
    items = data if isinstance(data, list) else [data]
    # Parse via Pydantic
    return [parser.parse(json.dumps(item)) for item in items]

def generate_profile(student_details: dict,roll_no: int):
    student_json_str = json.dumps(student_details, indent=2)
    response = chain.invoke({"student_json": student_json_str,"roll_no": roll_no})
    raw = getattr(response, "content", response)
    try:
        profiles = extract_and_parse(raw)
        return profiles[0] if profiles else None
    except Exception as e:
        print("Parsing/generation error:", e)
        return None

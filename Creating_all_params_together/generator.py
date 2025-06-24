from model_loader import load_llm
from prompt_builder import prompt, parser
from schema import StudentParameters
import re, json

llm = load_llm()
chain = prompt | llm

# def sanitize_json_string(text: str) -> str:
#     # Remove outer list if model returns JSON string inside a list
#     if isinstance(text, list) and len(text) == 1:
#         text = text[0]
#     # Clean escaped newlines and other format issues
#     text = text.replace("\\\n", "")
#     text = text.replace("\n", "")
#     text = text.replace("\\", "")
#     text = text.strip().strip("`")
#     return text



# def extract_json_blocks(text: str) -> list[str]:
#     json_pattern = re.compile(r'\{.*?\}(?=(\n|$))', re.DOTALL)
#     blocks = json_pattern.findall(text)
    
#     cleaned_blocks = []
#     for match in json_pattern.finditer(text):
#         block = match.group(0)
#         # Remove trailing commas or whitespace, clean up escaped characters
#         cleaned = block.strip().replace("\\n", "").replace("\\", "").strip("'")
#         try:
#             json.loads(cleaned)  # Validate
#             cleaned_blocks.append(cleaned)
#         except Exception as e:
#             print("Skipping invalid JSON block:", e)
#     return cleaned_blocks

# def generate_profiles(memory_profiles: list = None):
#     memory_block = json.dumps(memory_profiles, indent=2) if memory_profiles else "[]"
#     # print("Memory block:", memory_block)

#     raw = chain.invoke({"memory_block": memory_block})
#     raw = raw.content if hasattr(raw, 'content') else raw  # Handle different response types
#     # Handle list-wrapped string output
#     if isinstance(raw, list) and len(raw) == 1 and isinstance(raw[0], str):
#         raw = raw[0]

#     print("Raw output:", raw)

#     try:
#         # Sanitize common escape issues
#         if raw.startswith("'") or raw.startswith('"'):
#             raw = raw.strip("'").strip('"')  # Remove extra quotes around the JSON string

#         raw = raw.replace("\\n", "")  # remove literal \n
#         raw = raw.replace("\\\"", "\"")  # unescape double quotes
#         raw = raw.replace("\\'", "'")    # unescape single quotes
#         raw = raw.strip("`").strip()  # remove markdown or whitespace

#         # Wrap in array if it's a single object
#         if raw.startswith("{") and raw.endswith("}"):
#             raw = f"[{raw}]"

#         # Try parsing JSON
#         data = json.loads(raw)
#         print("Parsed JSON data:", data)
#         parsed_profiles = []
#         for entry in data:
#             try:
#                 parsed_profiles.append(parser.parse(json.dumps(entry)))
#             except Exception as sub_e:
#                 print("Error parsing one profile:", sub_e)
#         return parsed_profiles

#     except Exception as e:
#         print(f" Failed to parse response as JSON array or object: {e}")
#         return []

def extract_and_parse(raw: str):
    #  Remove markdown fences/backticks & BOM
    text = raw.lstrip('\ufeff').strip().strip('`').strip()
    # Grab the first JSON object or array
    match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object or array found in response")
    blob = match.group(1)
    # Clean common escapes
    blob = blob.replace('\\n', '').replace('\\"', '"').replace("\\'", "'")
    data = json.loads(blob)
    items = data if isinstance(data, list) else [data]
    return [parser.parse(json.dumps(item)) for item in items]

def generate_profiles(memory_profiles=None):
    memory_block = json.dumps(memory_profiles or [], indent=2)
    response = chain.invoke({ "memory_block": memory_block })
    raw = getattr(response, "content", response)
    try:
        profiles = extract_and_parse(raw)
        return profiles
    except Exception as e:
        print("Parsing/generation error:", e)
        return []




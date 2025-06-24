import re
import json
import pandas as pd
from langchain.schema import HumanMessage

from model_loader import load_llm
from prompt_builder2 import build_inputs
from schema2 import NextSectionRange
from config import OUTPUT_CSV

def sanitize_fence(text: str) -> str:
    # Strip leading/trailing whitespace
    t = text.strip()
    # Remove ```json or ``` on first line
    t = re.sub(r"^```(?:json)?\s*\n", "", t)
    # Remove closing ``` on last line
    t = re.sub(r"\n```$", "", t)
    return t.strip()

def main():
    #  Build prompt inputs, parser & PromptTemplate
    inputs, _, prompt_template = build_inputs()

    #  Render to single prompt string
    prompt_text = prompt_template.format(**inputs)

    #  Send to Gemini
    messages = [HumanMessage(content=prompt_text)]
    llm = load_llm()
    raw = llm.invoke(messages)

    #  Extract pure text
    raw_str = (
        raw.content
        if hasattr(raw, "content")
        else raw[0].content
        if isinstance(raw, list) and hasattr(raw[0], "content")
        else raw
    )

    #  Strip markdown fences
    clean = sanitize_fence(raw_str)

    #  Parse JSON
    try:
        json_list = json.loads(clean)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Cleaned output was not valid JSON:\n{clean}") from e

    #  Validate each entry with Pydantic
    validated = []
    for idx, entry in enumerate(json_list):
        try:
            validated.append(NextSectionRange.model_validate(entry))
        except Exception as e:
            raise RuntimeError(f"Validation failed for item #{idx}: {entry}") from e

    #  Dump to DataFrame & save
    df = pd.DataFrame([obj.model_dump() for obj in validated])
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(df)} section-range entries to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
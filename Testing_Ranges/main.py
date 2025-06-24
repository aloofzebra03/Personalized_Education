# main.py

import re
import json
import pandas as pd
from langchain.schema import HumanMessage

from model_loader import load_llm
from prompt_builder2 import build_inputs
from schema2 import NextSectionRange
from config import NEXT_SECTIONS, OUTPUT_CSV

def sanitize_fence(text: str) -> str:
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*\n", "", t)
    t = re.sub(r"\n```$", "", t)
    return t.strip()

def main():
    # Prepare static inputs
    inputs, parser, prompt_template = build_inputs()
    llm = load_llm()

    prev_ranges = []
    all_validated = []

    # Loop over each section and generate one disjoint range per call
    for section in NEXT_SECTIONS:
        payload = {
            "student_schema": inputs["student_schema"],
            "section_name": section,
            "prev_ranges": json.dumps(prev_ranges, indent=2),
            "sections_list": inputs["sections_list"]
        }

        # Render prompt & invoke LLM
        prompt_text = prompt_template.format(**payload)
        messages = [HumanMessage(content=prompt_text)]
        raw = llm.invoke(messages)
        cleaned = sanitize_fence(raw.content if hasattr(raw, "content") else raw)

        # Parse & validate exactly one object
        try:
            obj = json.loads(cleaned)
        except json.JSONDecodeError:
            raise RuntimeError(f"Output was not valid JSON:\n{cleaned}")

        entry = NextSectionRange.model_validate(obj)

        # Accumulate
        prev_ranges.append(entry.model_dump())
        all_validated.append(entry)

        print(f" Generated ranges for section: {section}")

    # Dump all to CSV
    df = pd.DataFrame([e.model_dump() for e in all_validated])
    df.to_csv(OUTPUT_CSV, index=False)
    print(f" Saved {len(df)} section-range entries to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

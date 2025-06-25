import os
import logging
import pandas as pd
from itertools import islice
from schema import parser
from prompt import get_prompt
from llm import get_remote_llm  # or get_hf_pipeline for local
from config import (
    PROFILES_CSV,
    QUESTIONS_TXT,
    OUTPUT_CSV
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chunked(iterable, size):
    it = iter(iterable)
    while True:
        batch = list(islice(it, size))
        if not batch:
            break
        yield batch


def format_profile(row: pd.Series) -> str:

    parts = []
    for col, val in row.items():
        parts.append(f"{col}: {val}")
    return "\n".join(parts)

def clean_answer(raw: str, question: str) -> str:
    """
    Remove any leading echo of the question (or anything before it),
    then strip out extra whitespace/punctuation.
    """
    # 1) If the model re-echoed the question, drop it
    idx = raw.lower().find(question.lower())
    if idx != -1:
        raw = raw[idx + len(question):]

    # 2) Remove leading colons, dashes, newlines, spaces
    return raw.lstrip(" :–—\n\t")


def run():
    df_profiles = pd.read_csv(PROFILES_CSV)
    with open(QUESTIONS_TXT) as f:
        questions = [q.strip() for q in f if q.strip()]

    # 1) Prepare output file: write header
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    # create empty DF with the right columns, write it out
    pd.DataFrame(columns=["student_name", "student_id", "question", "rag_answer"]) \
      .to_csv(OUTPUT_CSV, index=False)

    prompt = get_prompt()
    llm    = get_remote_llm()
    chain  = prompt | llm

    # 2) Loop profiles
    for idx, row in df_profiles.iterrows():
        prof_text    = format_profile(row)
        student_id   = idx
        student_name = row["name"]

        profile_rows = []
        for q in questions:
            out = chain.invoke({
                "student_id":   student_id,
                "student_name": student_name,
                "profile_text": prof_text,
                "question":     q
            })
            answer = out[0] if isinstance(out, list) else out
            profile_rows.append({
                "student_name": student_name,
                "student_id":   student_id,
                "question":     q,
                "rag_answer":   answer.strip()
            })

        # 3) Append *this* profile’s answers
        pd.DataFrame(profile_rows) \
            .to_csv(OUTPUT_CSV, mode="a", index=False, header=False)

        print(f"Done with profile {student_id}")

    logger.info("All done; results in %s", OUTPUT_CSV)
    print("All done; results in %s" % OUTPUT_CSV)

if __name__ == "__main__":
    run()

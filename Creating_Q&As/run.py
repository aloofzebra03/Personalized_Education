import pandas as pd
import json
import tqdm
from config import *
from models.model_loader import load_model
from prompts.prompt_builder import build_prompt_and_parser
from engine.qa_generator import generate_qas, batch_questions

def load_questions(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [q.strip() for q in f.readlines() if q.strip()]

def main():
    # Import student profiles and questions
    df = pd.read_csv(PROFILE_CSV_PATH)
    if 'student_id' not in df.columns:
        df['student_id'] = df.index
    all_questions = load_questions(QUESTION_LIST_PATH)
    question_batches = batch_questions(all_questions, batch_size=10)

    # Load LLM + prompt
    model = load_model()
    prompt, parser = build_prompt_and_parser()

    chain = prompt|model|parser
    all_qas = []

    # Generate answers for all students in batches of 10 questions
    for index, row in tqdm(df.iloc[0:1].iterrows(), total=len(df)):
        qas = generate_qas(index,row.to_dict(), question_batches, chain)
        all_qas.extend(qas)

    # Save as JSONL
    with open(OUTPUT_JSONL_PATH, "w", encoding="utf-8") as f:
        for item in all_qas:
            f.write(json.dumps(item) + "\n")

    # Save as CSV
    pd.DataFrame(all_qas).to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"\n Saved {len(all_qas)} Q&A pairs.")

if __name__ == "__main__":
    main()

import json
import time
import pandas as pd

from config import client, MODEL_NAME
from schemas import ScoreExplanation
import os
# from prompt import chain

def load_data(profiles_path: str, answers_path: str):
    profiles_df = pd.read_csv(profiles_path)
    answers_df  = pd.read_csv(answers_path)
    # group every 3 rows into a list of dicts
    qa_groups = [
        answers_df.iloc[i : i + 4][["question", "rag_answer"]]
                  .to_dict(orient="records")
        for i in range(0, len(answers_df), 4)
    ]
    return profiles_df, qa_groups

def generate_score_for_student(profile: dict, qas: list) -> ScoreExplanation:
    # print("Profile:", profile)
    # print("QAs:", qas)
    prompt = f"""
You are an expert AI tutor specialized in personalized education for students in grades 7–10.  
Your task is to evaluate a set of three question–answer pairs generated for a single student. Using only the information in the student’s profile, you will:

1. **Clean the Answer**  
   • Each provided “answer” may include artifacts, extra commentary, duplicate lines, or boilerplate (e.g. “LLM waiting for response from student,” repeated instructions, etc.).  
   • **Identify and discard any such noise**, then extract the core response content (the substantive explanation text) for your scoring.

2. **Assess Personalization**  
   • Assign an integer score from **1 (not personalized)** to **10 (highly personalized)**, reflecting how well the cleaned answer aligns with the student’s unique attributes—such as grade level, interests, learning goals, and accommodations.  
   • Provide a brief rationale citing which specific profile details informed your personalization judgment.

3. **Assess Relevance & Accuracy**  
   • Assign an integer score from **1 (off-topic or incorrect)** to **10 (perfectly on-topic and accurate)**, indicating how well the cleaned answer addresses the curriculum objectives and factual correctness.  
   • Provide a concise explanation of any content issues or scope mismatches.

Student Profile:
{json.dumps(profile)}

Generated Q&A:
{json.dumps(qas)}

Return ONLY a JSON object with keys:
- personalization_score (1–10)
- personalization_explanation
- relevance_score (1–10)
- relevance_explanation
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt],
        config={
            "response_mime_type": "application/json",
            "response_schema": ScoreExplanation,
        },
    )
    return ScoreExplanation.model_validate_json(response.text)

def run_all(
    profiles_path: str,
    answers_path:  str,
    out_detail:    str,
    out_summary:   str,
):
    os.makedirs(os.path.dirname(out_detail), exist_ok=True)
    os.makedirs(os.path.dirname(out_summary), exist_ok=True)

    profiles, qa_groups = load_data(profiles_path, answers_path)
    n = min(len(profiles), len(qa_groups))
    results = []

    for i in range(n):
        profile = profiles.iloc[i].to_dict()
        qas     = qa_groups[i]
        # Simple progress indicator
        print(f"Processing student {i+1}/{n}...")
        scored = generate_score_for_student(profile, qas)

        record = {
            **profile,
            "personalization_score": scored.personalization_score,
            "personalization_explanation": scored.personalization_explanation,
            "relevance_score": scored.relevance_score,
            "relevance_explanation": scored.relevance_explanation,
        }
        results.append(record)
        time.sleep(1.0)  # rate-limit

    # Save detailed per-student results
    df = pd.DataFrame(results)
    df.to_csv(out_detail, index=False)  # overwrites or creates anew
    print(f"Details written to {out_detail}")

    # Compute and save averages
    summary = {
        "avg_personalization_score": df["personalization_score"].mean(),
        "avg_relevance_score":       df["relevance_score"].mean(),
    }
    pd.DataFrame([summary]).to_csv(out_summary, index=False)
    print(f"Summary written to {out_summary}")

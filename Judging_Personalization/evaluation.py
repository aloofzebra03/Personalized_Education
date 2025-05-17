# evaluate_batch.py

import pandas as pd
from tqdm import tqdm
from model_loader import get_judge_llm
from judge_chain import build_judge_chain

# Load data
profiles_df = pd.read_csv("langchain_structured_profiles.csv")
qas_df = pd.read_csv("generated_qas.csv")

# Load Gemini judge and chain
llm = get_judge_llm()
chain = build_judge_chain(llm)

def format_profile(profile_row) -> str:
    return "\n".join([
        f"Name: {profile_row['name']}",
        f"Age: {profile_row['age']}",
        f"Class: {profile_row['class_level']} ({profile_row['syllabus']})",
        f"Interests: {profile_row['interests']}",
        f"Personality: {profile_row['personality']}",
        f"Hobbies: {profile_row['hobbies']}",
        f"Learning Style: {profile_row['learning_style']}",
        f"Study Routine: {profile_row['study_routine_start']} to {profile_row['study_routine_end']}",
        f"Preferred Subjects: {profile_row['preferred_subjects']}",
        f"Struggles: {profile_row['struggles_with']}",
        f"Strengths: {profile_row['strengths']}",
        f"Motivation Style: {profile_row['motivation_style']}",
        f"Tech Savviness: {profile_row['tech_savviness']}",
        f"Accomplishments: {profile_row['accomplishments']}",
        f"Teacher Feedback: {profile_row['teacher_feedback']}",
        f"Student Voice: {profile_row['student_voice']}",
        f"Interesting Stories: {profile_row['interesting_stories']}",
    ])

records = []

# Evaluate each Q&A pair with a progress bar
print("Starting batch evaluation...\n")
for idx, row in tqdm(qas_df.iterrows(), total=len(qas_df), desc="Evaluating"):
    student_id = row["student_id"]
    question = row["question"]
    tutor_answer = row["answer"]
    profile_row = profiles_df.iloc[student_id]
    profile_str = format_profile(profile_row)

    try:
        result = chain.invoke({
            "student_profile": profile_str,
            "question": question,
            "tutor_answer": tutor_answer
        })
        score = result.score
        explanation = result.explanation
    except Exception as e:
        score = None
        explanation = f"Error: {str(e)}"

    records.append({
        "student_id": student_id,
        "question": question,
        "answer": tutor_answer,
        "score": score,
        "explanation": explanation
    })

# Save per-question scores
results_df = pd.DataFrame(records)
results_df.to_csv("score_report.csv", index=False)

# Save per-student average scores
summary_df = results_df.groupby("student_id")["score"].mean().reset_index()
summary_df.rename(columns={"score": "avg_personalization_score"}, inplace=True)
summary_df.to_csv("student_score_summary.csv", index=False)

print("\n Evaluation complete!")
print("- Detailed results: score_report.csv")
print("- Per-student averages: student_score_summary.csv")

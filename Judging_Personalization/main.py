from processor import run_all

if __name__ == "__main__":
    run_all(
        profiles_path=  r"Judging_Personalization/data/langchain_structured_profiles.csv",
        answers_path= r"Judging_Personalization/data/finetune_personalized_answers.csv",
        out_detail=   r"Judging_Personalization/output/finetuned_scored_personalization_relevance.csv",
        out_summary=  r"Judging_Personalization/output/finetuned_summary_scores.csv",
    )

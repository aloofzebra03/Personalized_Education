from pydantic import BaseModel, Field

class ScoreExplanation(BaseModel):
    personalization_score: int = Field(..., ge=1, le=10, description="1–10 personalization score")
    personalization_explanation: str = Field(..., description="Rationale for personalization score")
    relevance_score:    int = Field(..., ge=1, le=10, description="1–10 relevance score")
    relevance_explanation: str = Field(..., description="Rationale for relevance score")

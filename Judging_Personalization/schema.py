from pydantic import BaseModel, Field

class PersonalizationEvaluation(BaseModel):
    score: int = Field(..., ge=1, le=5, description="Personalization score between 1 and 5")
    explanation: str = Field(..., description="Justification for the given score")

from pydantic import BaseModel, Field
from typing import List, Literal

class StudentParameters(BaseModel):
    conceptual_clarity_level: int = Field(..., ge=1, le=5)
    retention_strength: float = Field(..., ge=0.0, le=100.0)
    family_responsibilities_hrs: int = Field(..., ge=0, le=24)
    metacognitive_skill_level: int = Field(..., ge=1, le=5)
    ongoing_concept: Literal[
        'Sundial',
        'Water Clock',
        'Hourglass',
        'Candle Clock',
        'Simple Pendulum',
        'Time Period of Pendulum',
        'Speed',
        'SI Unit of Time',
        'Uniform Linear Motion',
        'Non-uniform Linear Motion'
        ] = Field(
            ...,
            description=(
                "Concept that the student is currently learning ."
            )
        )
    error_pattern: Literal['calculation','conceptual','careless']
    input_method_preference: Literal['typing','voice','writing']
    content_type_preference: List[str]

class NextSectionRange(BaseModel):
    section_name: str

    conceptual_clarity_level_min: int = Field(..., ge=1, le=5)
    conceptual_clarity_level_max: int = Field(..., ge=1, le=5)

    retention_strength_min: float = Field(..., ge=0.0, le=100.0)
    retention_strength_max: float = Field(..., ge=0.0, le=100.0)

    family_responsibilities_hrs_min: int = Field(..., ge=0, le=24)
    family_responsibilities_hrs_max: int = Field(..., ge=0, le=24)

    metacognitive_skill_level_min: int = Field(..., ge=1, le=5)
    metacognitive_skill_level_max: int = Field(..., ge=1, le=5)

    # ongoing_concept: List[Literal[
    #     'Sundial',
    #     'Water Clock',
    #     'Hourglass',
    #     'Candle Clock',
    #     'Simple Pendulum',
    #     'Time Period of Pendulum',
    #     'Speed',
    #     'SI Unit of Time',
    #     'Uniform Linear Motion',
    #     'Non-uniform Linear Motion'
    #     ]] = Field(
    #         ...,
    #         description=(
    #             "Concept that the student is currently learning.This may or may not be relevant to next section prediction.If not put all the possible ongoing concepts in each section."
    #         )
    #     )
    error_pattern: Literal['calculation','conceptual','careless']
    input_method_preference: Literal['typing','voice','writing']
    content_type_preference: List[str]

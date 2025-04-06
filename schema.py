from pydantic import BaseModel
from typing import List, Dict
from pydantic import Field
from typing import Literal

class StudentProfile(BaseModel):
    name: str
    age: int = Field(gt=12, lt=18)  # Age should be between 5 and 18
    class_level: int = Field(gt=7, lt=12)  # Class level should be between 1 and 12
    syllabus: Literal['CBSE', 'ICSE', 'IB', 'IGCSE']
    interests: List[str]
    personality: List[str]
    hobbies: List[str]
    learning_style: str
    preferred_subjects: List[str]
    struggles_with: str
    strengths: List[str]
    emotional_traits: str
    motivation_style: str
    group_behavior: str
    social_skills: str
    marks_last_year: Dict[str, int]
    marks_last_internals: Dict[str, int]
    teacher_feedback: str
    student_voice: str
    accomplishments: List[str]
    digital_learning: Dict[str, str]
    home_environment: Dict[str, str]
    interesting_stories: List[str]

from pydantic import BaseModel
from typing import List, Dict
from pydantic import Field
from typing import Literal

class StudentProfile(BaseModel):
    name: str = Field(description="Full name of the student")
    age: int = Field(gt=12, lt=18, description="Age of the student, between 13 and 17 inclusive")
    class_level: int = Field(gt=7, lt=12, description="Current class level of the student, between 8 and 11")
    syllabus: Literal['CBSE', 'ICSE', 'IB', 'IGCSE'] = Field(description="Educational syllabus the student is enrolled in")
    interests: List[str] = Field(description="List of areas or topics the student is genuinely interested in")
    personality: List[str] = Field(description="Personality traits such as introverted, curious, etc.")
    hobbies: List[str] = Field(description="Leisure activities the student enjoys doing outside school")
    learning_style: str = Field(description="Dominant learning style like Visual, Auditory, or Kinesthetic")
    preferred_subjects: List[str] = Field(description="Subjects the student enjoys and performs well in")
    struggles_with: str = Field(description="Subject or area the student finds most challenging")
    strengths: List[str] = Field(description="Academic or behavioral strengths the student demonstrates")
    emotional_traits: str = Field(description="Describes how the student emotionally interacts with feedback or school life")
    motivation_style: str = Field(description="What motivates the student—rewards, praise, recognition, etc.")
    group_behavior: str = Field(description="How the student behaves and contributes in group settings")
    social_skills: str = Field(description="Quality and type of social interactions and relationships")
    marks_last_year: Dict[str, int] = Field(description="Subject-wise academic scores from the previous year")
    marks_last_internals: Dict[str, int] = Field(description="Subject-wise internal test scores for the current year")
    teacher_feedback: str = Field(description="Summary of teacher's feedback on academic and behavioral performance")
    student_voice: str = Field(description="A self-reflective quote or opinion from the student")
    accomplishments: List[str] = Field(description="Notable achievements in academics, sports, or other activities")
    digital_learning: Dict[str, str] = Field(description="Digital learning preferences, tools used, and tech savviness")
    home_environment: Dict[str, str] = Field(description="Information about home learning support, internet, and languages spoken")
    interesting_stories: List[str] = Field(description="Anecdotal stories that give insight into the student's background and personality")

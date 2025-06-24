from pydantic import BaseModel,Field
from typing import List, Dict,Literal
from datetime import time

class StudentProfile(BaseModel):
    name: str = Field(description="Random indian full name of the student")
    age: int = Field(gt=12, lt=18, description="Random age of the student, between 13 and 17 inclusive")
    class_level: int = Field(gt=6, lt=13, description="Current class level of the student, between 7 and 12")
    syllabus: Literal['CBSE', 'ICSE', 'IB', 'IGCSE'] = Field(description="Educational syllabus the student is enrolled in")
    
    interests: List[str] = Field(description="List of areas or topics the student is genuinely interested in.Ensure that each element in the List is only a single word and not a sentence")
    personality: List[str] = Field(description="Personality traits such as introverted, curious, etc.Ensure that each element in the List is only a single word and not a sentence")
    
    hobbies: List[str] = Field(description="Leisure activities the student enjoys doing outside school.Ensure that each element in the List is only a single word and not a sentence")
    learning_style: List[str] = Field(description="Dominant learning style like Visual, Auditory, or Kinesthetic.There can be more.Ensure that you output is a list and each element in the List is only a single word and not a sentence.")
    pattern_of_learning: List[str] = Field(description="Preferred methods of learning such as reading, writing, or hands-on activitiesThere can be more.Ensure that you output is a list and each element in the List is only a single word and not a sentence")
    
    study_routine_start: str = Field(description="Start time of study routine")
    study_routine_end: str = Field(description="End time of study routine")
    
    preferred_subjects: List[str] = Field(description="Subjects the student enjoys studying.Ensure that each element in the List is only a single word and not a sentence")
    struggles_with: List[str] = Field(description="Subject or areas of a particular subject the student finds most challenging")
    strengths: List[str] = Field(description="Academic or behavioral strengths the student demonstrates.Ensure that each element in the List is only a single word and not a sentence")
    challenges: List[str] = Field(default_factory=list, description="Situations that pose difficulty (e.g., orals/vivas).There can be more than these.")

    academic_progress: str = Field(description="Narrative or metric of academic improvement")
    marks_last_year_final: dict[str,int] = Field(description="Subject-wise marks from last year's final exams")
    marks_last_internals: dict[str,int] = Field(description="Subject-wise marks from latest internal exams")

    emotional_traits: str = Field(description="Describes how the student emotionally interacts with feedback or school life")

    motivation_style: List[str] = Field(description="What motivates the student—rewards, praise, recognition, etc.Ensure that your output is a list and each element in the List is only a single word and not a sentence")
    group_behavior: str = Field(description="How the student behaves and contributes in group settings")
    social_skills: str = Field(description="Quality and type of social interactions and relationships")

    teacher_feedback: str = Field(description="Summary of teacher's feedback on academic and behavioral performance")
    student_voice: str = Field(description="A self-reflective quote or opinion from the student")

    accomplishments: List[str] = Field(description="Notable achievements in academics, sports, or other activities")
    digital_learning: List[str] = Field(description="Digital learning preferences, tools apps and platforms used")
    
    tech_savviness: Literal['High','Medium','Low'] = Field(description="Level of comfort and skills with technology.Choose one from the 3 options High,Medium,Low only")

    home_environment: List[str] = Field(description="Information about home learning support, internet, and languages spoken")
    
    interesting_stories: str = Field(description="Anecdotal stories that give insight into the student's background and personality")

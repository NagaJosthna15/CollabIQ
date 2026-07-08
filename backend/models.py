from pydantic import BaseModel
from typing import List

class Student(BaseModel):
    name: str
    email: str
    cgpa: float
    skills: List[str]
    interests: List[str]
    projects_completed: int

class Project(BaseModel):
    title: str
    description: str
    required_skills: list[str]
    team_size: int
    created_by: str    
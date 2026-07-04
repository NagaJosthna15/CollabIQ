from pydantic import BaseModel
from typing import List

class Student(BaseModel):
    name: str
    email: str
    cgpa: float
    skills: List[str]
    interests: List[str]
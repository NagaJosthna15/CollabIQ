from pydantic import BaseModel
from typing import List

class Student(BaseModel):
    name: str
    email: str
    cgpa: float
    skills: List[str]
    interests: List[str]
    projects_completed: int
    github_username: str

class Project(BaseModel):
    title: str
    description: str
    required_skills: list[str]
    team_size: int 
class StudentRegister(BaseModel):
    name: str
    email: str
    password: str
    cgpa: float
    skills: List[str]
    interests: List[str]
    projects_completed: int
    github_username: str
class RecruiterRegister(BaseModel):
    name: str
    email: str
    password: str    


class StudentLogin(BaseModel):
    email: str
    password: str 
class StudentProfileUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    cgpa: float | None = None
    skills: List[str] | None = None
    interests: List[str] | None = None
    projects_completed: int | None = None
    github_username: str | None = None         
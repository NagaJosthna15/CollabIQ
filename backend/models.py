from pydantic import BaseModel, EmailStr, Field
from typing import List

class Student(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    cgpa: float = Field(ge=0, le=10)
    skills: List[str] = Field(min_length=1)
    interests: List[str] = Field(min_length=1)
    projects_completed: int = Field(ge=0)
    github_username: str = Field(min_length=1)

class Project(BaseModel):
    title: str = Field(min_length=2)
    description: str = Field(min_length=10)
    required_skills: list[str] = Field(min_length=1)
    team_size: int = Field(ge=1)

class StudentRegister(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=8)
    cgpa: float = Field(ge=0, le=10)
    skills: List[str] = Field(min_length=1)
    interests: List[str] = Field(min_length=1)
    projects_completed: int = Field(ge=0)
    github_username: str = Field(min_length=1)

class RecruiterRegister(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=8)

class StudentLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class StudentProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2)
    email: EmailStr | None = None
    cgpa: float | None = Field(default=None, ge=0, le=10)
    skills: List[str] | None = Field(default=None, min_length=1)
    interests: List[str] | None = Field(default=None, min_length=1)
    projects_completed: int | None = Field(default=None, ge=0)
    github_username: str | None = Field(default=None, min_length=1)
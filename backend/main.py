from fastapi import FastAPI
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from models import Student, Project
from database import students_collection, projects_collection
from fastapi import UploadFile, File
from services.skill_extractor import extract_skills
from bson import ObjectId
from services.matcher import calculate_match_score
from services.team_optimizer import create_team
from services.talent_scorer import calculate_talent_score
from services.ranker import calculate_final_score
from services.github_analyzer import (
    get_github_profile,
    get_github_repositories
)
from services.github_relevance import (
    calculate_github_relevance
)
from services.recruiter_agent import RecruiterAgent
from services.student_intelligence import (
    build_student_profile
)
from services.team_success import (
    calculate_team_success
)
import shutil
def make_json_safe(value):
    if isinstance(value, ObjectId):
        return str(value)

    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            make_json_safe(item)
            for item in value
        ]

    return value

app = FastAPI(
    title="CollabIQ API",
    description="Intelligent Collaboration & Team Optimization Platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to CollabIQ 🚀"
    }

@app.post("/students")
def create_student(student: Student):

    student_data = student.dict()

    result = students_collection.insert_one(
        student_data
    )

    return {
        "message": "Student added successfully",
        "id": str(result.inserted_id)
    }

@app.get("/students")
def get_students():

    students = []

    for student in students_collection.find():

        student["_id"] = str(student["_id"])

        students.append(student)

    return students

@app.post("/upload-resume/{student_id}")
async def upload_resume(
    student_id: str,
    file: UploadFile = File(...)
):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    skills = extract_skills(
        file_path
    )

    result = students_collection.update_one(
        {
            "_id": ObjectId(student_id)
        },
        {
            "$set": {
                "resume_skills": skills
            }
        }
    )

    return {
        "filename": file.filename,
        "skills": skills,
        "updated": result.modified_count
    }

@app.post("/projects")
def create_project(project: Project):

    project_data = project.dict()

    result = projects_collection.insert_one(
        project_data
    )

    return {
        "message": "Project created successfully",
        "project_id": str(result.inserted_id)
    }

@app.get("/projects")
def get_projects():

    projects = []

    for project in projects_collection.find():

        project["_id"] = str(
            project["_id"]
        )

        projects.append(project)

    return projects

@app.get("/projects/{project_id}/matches")
def find_matches(project_id: str):

    project = projects_collection.find_one(
        {
            "_id": ObjectId(project_id)
        }
    )

    if not project:
        return {
            "message": "Project not found"
        }

    required_skills = project[
        "required_skills"
    ]

    matches = []

    for student in students_collection.find():

        resume_skills = student.get(
            "resume_skills",
            []
        )

        score = calculate_match_score(
            resume_skills,
            required_skills
        )

        talent_score = calculate_talent_score(
            student
        )

        final_score = calculate_final_score(
            score,
            talent_score
        )

        matches.append({
            "student_name": student["name"],
            "match_score": score,
            "talent_score": talent_score,
            "final_score": final_score
        })

    matches.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return matches

@app.get("/projects/{project_id}/team")
def generate_team(project_id: str):

    project = projects_collection.find_one(
        {
            "_id": ObjectId(project_id)
        }
    )

    if not project:
        return {
            "message": "Project not found"
        }

    required_skills = project[
        "required_skills"
    ]

    matches = []

    for student in students_collection.find():

        resume_skills = student.get(
            "resume_skills",
            []
        )

        score = calculate_match_score(
            resume_skills,
            required_skills
        )

        matches.append({
            "student_name": student["name"],
            "match_score": score
        })

    team = create_team(
        matches,
        project["team_size"]
    )

    return {
        "project": project["title"],
        "team": team
    }

@app.get("/students/{student_id}/talent-score")
def get_talent_score(student_id: str):

    student = students_collection.find_one(
        {
            "_id": ObjectId(student_id)
        }
    )

    if not student:
        return {
            "message": "Student not found"
        }

    score = calculate_talent_score(
        student
    )

    return {
        "student": student["name"],
        "talent_score": score
    }

@app.get("/students/{student_id}/github-profile")
def github_profile(student_id: str):

    student = students_collection.find_one(
        {
            "_id": ObjectId(student_id)
        }
    )

    if not student:
        return {
            "message": "Student not found"
        }

    username = student.get(
        "github_username"
    )

    if not username:
        return {
            "message": "GitHub username not found"
        }

    profile = get_github_profile(
        username
    )

    return profile

@app.get("/students/{student_id}/github-projects")
def github_projects(student_id: str):

    student = students_collection.find_one(
        {
            "_id": ObjectId(student_id)
        }
    )

    if not student:
        return {
            "message": "Student not found"
        }

    username = student.get(
        "github_username"
    )

    repos = get_github_repositories(
        username
    )

    return {
        "username": username,
        "repositories": repos
    }

@app.get(
    "/projects/{project_id}/github-relevance/{student_id}"
)
def github_relevance(
    project_id: str,
    student_id: str
):

    project = projects_collection.find_one(
        {
            "_id": ObjectId(project_id)
        }
    )

    student = students_collection.find_one(
        {
            "_id": ObjectId(student_id)
        }
    )

    if not project:
        return {
            "message": "Project not found"
        }

    if not student:
        return {
            "message": "Student not found"
        }

    username = student.get(
        "github_username"
    )

    repositories = get_github_repositories(
        username
    )

    score = calculate_github_relevance(
        repositories,
        project["required_skills"]
    )

    return {
        "student": student["name"],
        "project": project["title"],
        "github_relevance_score": score
    }

@app.get("/projects/{project_id}/smart-team")
def smart_team(project_id: str):

    project = projects_collection.find_one(
        {
            "_id": ObjectId(project_id)
        }
    )

    if not project:
        return {
            "message": "Project not found"
        }

    agent = RecruiterAgent()

    result = agent.recruit_team(
        project["title"],
        project.get("description", "")
    )

    return make_json_safe({ 
        "project": project["title"],
        "team": result["final_team"],
        "coverage": result["coverage"],
        "skill_gaps": result["skill_gaps"],
        "additional_candidates": result[
            "additional_candidates"
        ]
    })

@app.get(
    "/projects/{project_id}/team-success"
)
def team_success(
    project_id: str
):

    project = projects_collection.find_one(
        {
            "_id": ObjectId(project_id)
        }
    )

    if not project:
        return {
            "message": "Project not found"
        }

    agent = RecruiterAgent()

    recruitment_result = agent.recruit_team(
        project["title"],
        project.get("description", "")
    )

    team = recruitment_result[
        "final_team"
    ]

    result = calculate_team_success(
        team
    )

    return jsonable_encoder({
        "project": project["title"],
        "team_size": len(team),
        "success_score": result[
            "success_score"
        ],
        "success_probability": result[
            "success_probability"
        ]
    })

@app.get(
    "/students/{student_id}/intelligence-profile"
)
def get_intelligence_profile(
    student_id: str
):

    student = students_collection.find_one(
        {
            "_id": ObjectId(student_id)
        }
    )

    if not student:
        return {
            "error": "Student not found"
        }

    github_username = student.get(
        "github_username"
    )

    if not github_username:
        return {
            "error": "GitHub username not found"
        }

    profile = build_student_profile(
        github_username
    )

    return profile
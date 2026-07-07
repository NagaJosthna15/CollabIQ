from fastapi import FastAPI
from models import Student
from database import students_collection
from fastapi import UploadFile, File
from services.skill_extractor import extract_skills
from bson import ObjectId
from models import Student, Project
from database import students_collection, projects_collection
from services.matcher import calculate_match_score
from services.team_optimizer import create_team
import shutil

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

    result = students_collection.insert_one(student_data)

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
        shutil.copyfileobj(file.file, buffer)

    skills = extract_skills(file_path)

    result = students_collection.update_one(
        {"_id": ObjectId(student_id)},
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

    result = projects_collection.insert_one(project_data)

    return {
        "message": "Project created successfully",
        "project_id": str(result.inserted_id)
    }

@app.get("/projects")
def get_projects():

    projects = []

    for project in projects_collection.find():

        project["_id"] = str(project["_id"])

        projects.append(project)

    return projects

@app.get("/projects/{project_id}/matches")
def find_matches(project_id: str):

    project = projects_collection.find_one(
        {"_id": ObjectId(project_id)}
    )

    if not project:
        return {"message": "Project not found"}

    required_skills = project["required_skills"]

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

    matches.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return matches

@app.get("/projects/{project_id}/team")
def generate_team(project_id: str):

    project = projects_collection.find_one(
        {"_id": ObjectId(project_id)}
    )

    if not project:
        return {
            "message": "Project not found"
        }

    required_skills = project["required_skills"]

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
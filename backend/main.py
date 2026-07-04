from fastapi import FastAPI
from models import Student
from database import students_collection

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
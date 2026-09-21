import os
import bcrypt
from datetime import datetime, timedelta, timezone

from jose import jwt
from dotenv import load_dotenv
from bson import ObjectId

from database import students_collection

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is missing from .env")


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, password_hash):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def create_access_token(student_id):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_EXPIRE_MINUTES
    )

    payload = {
        "student_id": str(student_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


def register_student(student_data):
    email = student_data["email"].strip().lower()

    existing_student = students_collection.find_one({
        "email": email
    })

    if existing_student:
        return {
            "success": False,
            "message": "Student with this email already exists"
        }

    student_data["email"] = email
    student_data["password_hash"] = hash_password(
        student_data.pop("password")
    )
    student_data["created_at"] = datetime.now(timezone.utc)

    result = students_collection.insert_one(
        student_data
    )

    return {
        "success": True,
        "message": "Student registered successfully",
        "student_id": str(result.inserted_id)
    }


def login_student(email, password):
    email = email.strip().lower()

    student = students_collection.find_one({
        "email": email
    })

    if not student:
        return {
            "success": False,
            "message": "Invalid email or password"
        }

    password_hash = student.get("password_hash")

    if not password_hash:
        return {
            "success": False,
            "message": "This student account is not configured for login"
        }

    if not verify_password(
        password,
        password_hash
    ):
        return {
            "success": False,
            "message": "Invalid email or password"
        }

    token = create_access_token(
        student["_id"]
    )

    return {
        "success": True,
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "student_id": str(student["_id"]),
        "student_name": student.get("name")
    }


def get_student_from_token(token):
    payload = jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM]
    )

    student_id = payload.get("student_id")

    if not student_id:
        return None

    student = students_collection.find_one({
        "_id": ObjectId(student_id)
    })

    return student
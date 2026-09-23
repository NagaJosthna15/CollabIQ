from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId

from models import (
    Student,
    Project,
    StudentRegister,
    StudentLogin,
    StudentProfileUpdate,
    RecruiterRegister
)

from database import (
    students_collection,
    projects_collection,
    invitations_collection
)

from services.skill_extractor import extract_skills
from services.matcher import calculate_match_score
from services.team_optimizer import create_team
from services.talent_scorer import calculate_talent_score
from services.ranker import calculate_final_score

from services.github_analyzer import (
    get_github_profile,
    get_github_repositories
)

from services.github_relevance import calculate_github_relevance
from services.recruiter_agent import RecruiterAgent
from services.student_intelligence import build_student_profile
from services.team_success import calculate_team_success

from services.invitation_service import (
    create_invitation,
    accept_invitation,
    reject_invitation
)

from services.auth_service import (
    register_student,
    register_recruiter,
    login_student,
    get_student_from_token,
    update_student_profile
)

from services.student_project_service import (
    get_student_invitations,
    get_student_accepted_projects
)

from services.project_invitation_service import (
    get_project_invitations,
    get_project_candidate_status
)

from services.invitation_expiry_service import expire_pending_invitations

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


security = HTTPBearer(
    scheme_name="Bearer"
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        user = get_student_from_token(
            credentials.credentials
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


def require_role(role):
    def role_checker(
        user=Depends(get_current_user)
    ):
        user_role = user.get(
            "role",
            "student"
        )

        if user_role != role:
            raise HTTPException(
                status_code=403,
                detail=f"{role.capitalize()} access required"
            )

        return user

    return role_checker
def require_project_owner(project_id, recruiter):
    try:
        project_object_id = ObjectId(project_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid project ID"
        )

    project = projects_collection.find_one({
        "_id": project_object_id
    })

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if str(project.get("created_by")) != str(recruiter["_id"]):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this project"
        )

    return project


@app.get("/")
def home():
    return {
        "message": "Welcome to CollabIQ 🚀"
    }


@app.post("/auth/register")
def register(student: StudentRegister):
    student_data = student.model_dump()

    result = register_student(
        student_data
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


@app.post("/auth/recruiter/register")
def recruiter_register(
    recruiter: RecruiterRegister
):
    recruiter_data = recruiter.model_dump()

    result = register_recruiter(
        recruiter_data
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result


@app.post("/auth/login")
def login(student: StudentLogin):
    result = login_student(
        student.email,
        student.password
    )

    if not result["success"]:
        raise HTTPException(
            status_code=401,
            detail=result["message"]
        )

    return result


@app.get("/auth/me")
def get_current_student(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        student = get_student_from_token(
            credentials.credentials
        )

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        student["_id"] = str(
            student["_id"]
        )

        student.pop(
            "password_hash",
            None
        )

        return student

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


@app.get("/students/me")
def get_my_profile(
    student=Depends(
        require_role("student")
    )
):
    student["_id"] = str(
        student["_id"]
    )

    student.pop(
        "password_hash",
        None
    )

    return student


@app.put("/students/me")
def update_my_profile(
    profile: StudentProfileUpdate,
    student=Depends(
        require_role("student")
    )
):
    result = update_student_profile(
        str(student["_id"]),
        profile.model_dump(
            exclude_none=True
        )
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    result["student"]["_id"] = str(
        result["student"]["_id"]
    )

    result["student"].pop(
        "password_hash",
        None
    )

    return result


@app.get("/students/me/invitations")
def get_my_invitations(
    student=Depends(
        require_role("student")
    )
):
    invitations = get_student_invitations(
        str(student["_id"])
    )

    return make_json_safe({
        "student_name": student.get("name"),
        "total_invitations": len(invitations),
        "invitations": invitations
    })


@app.get("/students/me/accepted-projects")
def get_my_accepted_projects(
    student=Depends(
        require_role("student")
    )
):
    projects = get_student_accepted_projects(
        str(student["_id"])
    )

    return make_json_safe({
        "student_name": student.get("name"),
        "total_projects": len(projects),
        "projects": projects
    })


@app.post("/students")
def create_student(
    student: Student,
    recruiter=Depends(
        require_role("recruiter")
    )
):
    student_data = student.model_dump()

    result = students_collection.insert_one(
        student_data
    )

    return {
        "message": "Student added successfully",
        "id": str(result.inserted_id)
    }


@app.get("/students")
def get_students(
    recruiter=Depends(
        require_role("recruiter")
    )
):
    students = []

    for student in students_collection.find():
        student["_id"] = str(
            student["_id"]
        )

        student.pop(
            "password_hash",
            None
        )

        students.append(student)

    return students


@app.post("/upload-resume/{student_id}")
async def upload_resume(
    student_id: str,
    file: UploadFile = File(...),
    student=Depends(
        require_role("student")
    )
):
    if str(student["_id"]) != str(student_id):
        raise HTTPException(
            status_code=403,
            detail="You can only upload your own resume"
        )

    file_path = f"uploads/{file.filename}"

    with open(
        file_path,
        "wb"
    ) as buffer:
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
def create_project(
    project: Project,
    recruiter=Depends(
        require_role("recruiter")
    )
):
    project_data = project.model_dump()

    project_data["created_by"] = str(
        recruiter["_id"]
    )

    result = projects_collection.insert_one(
        project_data
    )

    return {
        "message": "Project created successfully",
        "project_id": str(
            result.inserted_id
        )
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
def find_matches(
    project_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
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
def generate_team(
    project_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
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
def get_talent_score(
    student_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
):
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
def github_profile(
    student_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
):
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
def github_projects(
    student_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
):
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
    student_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
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
def smart_team(
    project_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
):
    project = require_project_owner(
        project_id,
        recruiter
    )

    agent = RecruiterAgent()

    result = agent.recruit_team(
        project["title"],
        project.get(
            "description",
            ""
        )
    )

    team = result["final_team"]

    return make_json_safe({
        "project": project["title"],
        "team_size": len(team),
        "team": team,
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
    project_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
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
        project.get(
            "description",
            ""
        )
    )

    team = recruitment_result[
        "final_team"
    ]

    result = calculate_team_success(
        team
    )

    return make_json_safe({
        "project": project["title"],
        "team_size": len(team),
        "success_score": result[
            "success_score"
        ],
        "success_probability": result[
            "success_probability"
        ],
        "skill_coverage": result[
            "skill_coverage"
        ],
        "role_balance": result[
            "role_balance"
        ],
        "team_compatibility": result[
            "team_compatibility"
        ],
        "risk_level": result[
            "risk_level"
        ],
        "risks": result["risks"],
        "recommendations": result[
            "recommendations"
        ]
    })


@app.get(
    "/students/{student_id}/intelligence-profile"
)
def get_intelligence_profile(
    student_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
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


@app.post(
    "/projects/{project_id}/invite-candidates"
)
def invite_candidates(
    project_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
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

    result = agent.recruit_team(
        project["title"],
        project.get(
            "description",
            ""
        )
    )

    team = result.get(
        "final_team",
        []
    )

    invitations = []

    invitation_base_url = (
        "http://127.0.0.1:8000/invitations/respond"
    )

    for member in team:
        candidate = member.get(
            "candidate",
            {}
        )

        profile = candidate.get(
            "profile",
            {}
        )

        role = (
            member.get("role")
            or profile.get(
                "recommended_role"
            )
            or "Project Team Member"
        )

        candidate_id = (
            profile.get("student_id")
            or profile.get("_id")
            or profile.get("id")
        )

        existing_invitation = invitations_collection.find_one({
            "project_id": str(project_id),
            "candidate_id": str(candidate_id)
        })

        if existing_invitation:
            invitations.append({
                "candidate_name": (
                    profile.get("student")
                    or profile.get("name")
                ),
                "candidate_email": profile.get(
                    "email"
                ),
                "role": role,
                "status": "skipped",
                "reason": (
                    f"Already "
                    f"{existing_invitation.get('status')} "
                    f"for this project"
                ),
                "invitation_id": str(
                    existing_invitation["_id"]
                )
            })

            continue

        try:
            invitation = create_invitation(
                project_id=str(project_id),
                project_title=project["title"],
                candidate=candidate,
                role=role,
                invitation_link=invitation_base_url
            )

            invitations.append({
                "candidate_name": invitation[
                    "candidate_name"
                ],
                "candidate_email": invitation[
                    "candidate_email"
                ],
                "role": invitation["role"],
                "status": invitation["status"],
                "invitation_id": invitation["_id"]
            })

        except Exception as e:
            invitations.append({
                "candidate_name": (
                    profile.get("student")
                    or profile.get("name")
                ),
                "candidate_email": profile.get(
                    "email"
                ),
                "role": role,
                "status": "failed",
                "error": str(e)
            })

    return make_json_safe({
        "project": project["title"],
        "team_size": len(team),
        "invitations_sent": len([
            item
            for item in invitations
            if item["status"] == "invited"
        ]),
        "invitations": invitations
    })


@app.get(
    "/projects/{project_id}/invitations"
)
def get_project_invitation_status(
    project_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
):
    project = projects_collection.find_one(
        {
            "_id": ObjectId(project_id)
        }
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    result = get_project_invitations(
        project_id
    )

    return make_json_safe({
        "project": project["title"],
        "total_invitations": result[
            "total_invitations"
        ],
        "invited": result["invited"],
        "accepted": result["accepted"],
        "rejected": result["rejected"],
        "expired": result["expired"],
        "invitations": result["invitations"]
    })


@app.get(
    "/projects/{project_id}/candidate-status"
)
def get_project_candidate_status_api(
    project_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
):
    project = projects_collection.find_one(
        {
            "_id": ObjectId(project_id)
        }
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    result = get_project_candidate_status(
        project_id
    )

    return make_json_safe({
        "project": project["title"],
        "total_candidates": result[
            "total_candidates"
        ],
        "invited": result["invited"],
        "accepted": result["accepted"],
        "rejected": result["rejected"],
        "expired": result["expired"],
        "candidates": result["candidates"]
    })


@app.post(
    "/projects/{project_id}/expire-invitations"
)
def expire_project_invitations(
    project_id: str,
    recruiter=Depends(
        require_role("recruiter")
    )
):
    project = projects_collection.find_one(
        {
            "_id": ObjectId(project_id)
        }
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    result = expire_pending_invitations(
        project_id=project_id
    )

    return make_json_safe({
        "project": project["title"],
        "expired_count": result[
            "expired_count"
        ],
        "expiry_hours": result[
            "expiry_hours"
        ],
        "checked_at": result[
            "checked_at"
        ]
    })


@app.post(
    "/invitations/{token}/accept"
)
def accept_invitation_api(
    token: str
):
    result = accept_invitation(
        token
    )

    return make_json_safe(
        result
    )


@app.post(
    "/invitations/{token}/reject"
)
def reject_invitation_api(
    token: str
):
    result = reject_invitation(
        token
    )

    return make_json_safe(
        result
    )
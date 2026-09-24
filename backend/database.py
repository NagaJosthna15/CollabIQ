from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017"
)

db = client["collabiq_db"]

students_collection = db["students"]
projects_collection = db["projects"]
invitations_collection = db["invitations"]

students_collection.create_index(
    "email"
)

invitations_collection.create_index(
    "token"
)

invitations_collection.create_index(
    "project_id"
)

invitations_collection.create_index(
    "candidate_id"
)

invitations_collection.create_index(
    "status"
)

invitations_collection.create_index(
    [
        ("project_id", 1),
        ("created_at", -1)
    ]
)
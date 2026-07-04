from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["collabiq_db"]

students_collection = db["students"]
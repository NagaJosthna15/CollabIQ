from database import students_collection


def get_all_students():
    """
    Fetch all students from MongoDB.
    """
    return list(students_collection.find())


def get_student_by_id(student_id):
    """
    Fetch a single student by ID.
    """
    return students_collection.find_one({"_id": student_id})
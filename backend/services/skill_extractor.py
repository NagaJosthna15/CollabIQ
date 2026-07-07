from pypdf import PdfReader

SKILLS_DB = [
    "python",
    "java",
    "c",
    "c++",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "react",
    "nodejs",
    "mongodb",
    "sql",
    "power bi",
    "tableau",
    "excel",
    "fastapi",
    "flask",
    "javascript",
    "html",
    "css"
]

def extract_skills(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))
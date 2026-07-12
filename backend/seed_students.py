from database import students_collection

students = [

    {
        "name": "Sobha Sri",
        "email": "sobhasri05@gmail.com",
        "cgpa": 8.5,
        "skills": ["Python", "Machine Learning", "TensorFlow"],
        "interests": ["AI", "Data Science"],
        "projects_completed": 6,
        "github_username": "sobhasri",
        "resume_skills": [
            "python",
            "machine learning",
            "tensorflow",
            "sql",
            "pandas"
        ]
    },

    {
        "name": "Arjun Kumar",
        "email": "arjun@gmail.com",
        "cgpa": 8.5,
        "skills": ["React", "JavaScript", "CSS"],
        "interests": ["Frontend Development"],
        "projects_completed": 5,
        "github_username": "arjunkumar",
        "resume_skills": [
            "react",
            "javascript",
            "css",
            "html",
            "typescript"
        ]
    },

    {
        "name": "Rahul Sharma",
        "email": "rahul@gmail.com",
        "cgpa": 8.2,
        "skills": ["Java", "Spring Boot", "SQL"],
        "interests": ["Backend Development"],
        "projects_completed": 7,
        "github_username": "rahulsharma",
        "resume_skills": [
            "java",
            "spring boot",
            "sql",
            "mysql",
            "rest api"
        ]
    },

    {
        "name": "Sneha Patel",
        "email": "sneha@gmail.com",
        "cgpa": 8.9,
        "skills": ["React", "TypeScript", "Next.js"],
        "interests": ["Frontend Development"],
        "projects_completed": 4,
        "github_username": "snehapatel",
        "resume_skills": [
            "react",
            "typescript",
            "nextjs",
            "css"
        ]
    },

    {
        "name": "Vikram Rao",
        "email": "vikram@gmail.com",
        "cgpa": 8.0,
        "skills": ["Node.js", "MongoDB", "Express"],
        "interests": ["Backend Development"],
        "projects_completed": 6,
        "github_username": "vikramrao",
        "resume_skills": [
            "nodejs",
            "mongodb",
            "express",
            "javascript"
        ]
    },

    {
        "name": "Keerthi Nair",
        "email": "keerthi@gmail.com",
        "cgpa": 9.3,
        "skills": ["Power BI", "Excel", "SQL"],
        "interests": ["Data Analytics"],
        "projects_completed": 5,
        "github_username": "keerthinair",
        "resume_skills": [
            "power bi",
            "excel",
            "sql",
            "tableau"
        ]
    },

    {
        "name": "Rohit Verma",
        "email": "rohit@gmail.com",
        "cgpa": 8.4,
        "skills": ["Python", "Data Analysis", "SQL"],
        "interests": ["Analytics"],
        "projects_completed": 4,
        "github_username": "rohitverma",
        "resume_skills": [
            "python",
            "sql",
            "excel",
            "power bi"
        ]
    },

    {
        "name": "Ananya Singh",
        "email": "ananya@gmail.com",
        "cgpa": 8.8,
        "skills": ["React", "Node.js", "MongoDB"],
        "interests": ["Full Stack Development"],
        "projects_completed": 8,
        "github_username": "ananyasingh",
        "resume_skills": [
            "react",
            "nodejs",
            "mongodb",
            "javascript"
        ]
    },

    {
        "name": "Kiran Teja",
        "email": "kiran@gmail.com",
        "cgpa": 8.7,
        "skills": ["React", "Node.js", "PostgreSQL"],
        "interests": ["Full Stack Development"],
        "projects_completed": 5,
        "github_username": "kiranteja",
        "resume_skills": [
            "react",
            "nodejs",
            "postgresql",
            "javascript"
        ]
    }

]

students_collection.insert_many(students)

print("✅ 9 students inserted successfully")
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from services.llm.llm_project_analyzer import (
    analyze_project_with_llm
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

DOMAIN_PROFILES = {
    "Artificial Intelligence":
    "Projects involving AI agents, intelligent systems, reasoning and decision making",

    "Machine Learning":
    "Projects involving prediction models, data science, deep learning and ML algorithms",

    "Healthcare":
    "Projects related to patient monitoring, disease prediction, hospitals and healthcare technology",

    "Data Analytics":
    "Projects involving dashboards, business intelligence, analytics and reporting",

    "Web Development":
    "Projects involving websites, frontend, backend, APIs and web applications",

    "Cybersecurity":
    "Projects involving security, threat detection, privacy and cyber defense",

    "Cloud Computing":
    "Projects involving cloud platforms, deployment, scalability and infrastructure",

    "Automation":
    "Projects involving workflow automation, bots and productivity systems",

    "FinTech":
    "Projects related to banking, finance, payments and financial technology"
}
INNOVATION_PROFILES = [
    "Projects solving real world problems",

    "Artificial intelligence and machine learning systems",

    "Automation and productivity improvement systems",

    "Prediction, recommendation and optimization platforms",

    "Analytics and decision support systems"
]
COMPLEXITY_PROFILES = [
    "Simple application with basic functionality",

    "Application with APIs and database integration",

    "Full stack application with authentication and backend services",

    "Machine learning system with prediction models and analytics",

    "Large scale software platform with AI, databases, APIs and automation"
]

def detect_domain(readme_text):

    readme_embedding = model.encode(
        readme_text
    )

    scores = {}

    for domain, description in DOMAIN_PROFILES.items():

        domain_embedding = model.encode(
            description
        )

        similarity = cos_sim(
            readme_embedding,
            domain_embedding
        )

        scores[domain] = float(similarity)

    sorted_domains = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_domains = [
        domain
        for domain, score in sorted_domains[:3]
    ]

    return {
        "top_domains": top_domains
    }
def calculate_innovation_score(readme_text):

    readme_embedding = model.encode(
        readme_text
    )

    total_similarity = 0

    for profile in INNOVATION_PROFILES:

        profile_embedding = model.encode(
            profile
        )

        similarity = cos_sim(
            readme_embedding,
            profile_embedding
        )

        total_similarity += float(
            similarity
        )

    average_similarity = (
        total_similarity
        /
        len(INNOVATION_PROFILES)
    )

    innovation_score = round(
        average_similarity * 100,
        2
    )

    return innovation_score
def calculate_complexity_score(readme_text):

    readme_embedding = model.encode(
        readme_text
    )

    similarities = []

    for profile in COMPLEXITY_PROFILES:

        profile_embedding = model.encode(
            profile
        )

        similarity = cos_sim(
            readme_embedding,
            profile_embedding
        )

        similarities.append(
            float(similarity)
        )

    complexity_score = round(
        max(similarities) * 100,
        2
    )

    return complexity_score
def analyze_project(readme_text):

    domains = detect_domain(
        readme_text
    )

    innovation_score = (
        calculate_innovation_score(
            readme_text
        )
    )

    complexity_score = (
        calculate_complexity_score(
            readme_text
        )
    )
    llm_analysis = analyze_project_with_llm(
    readme_text
)

    return {
    "top_domains": domains ["top_domains"],
    "innovation_score":
    innovation_score,

    "complexity_score":
    complexity_score,

    "project_summary":
    llm_analysis[
        "project_summary"
    ],

    "industry_impact":
    llm_analysis[
        "industry_impact"
    ],

    "future_scope":
    llm_analysis[
        "future_scope"
    ],

    "innovation_level":
    llm_analysis[
        "innovation_level"
    ]
}
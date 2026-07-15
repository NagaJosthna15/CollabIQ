DOMAIN_KEYWORDS = [
    "artificial intelligence",
    "ai",
    "machine learning",
    "deep learning",
    "nlp",
    "computer vision",
    "healthcare",
    "fintech",
    "cybersecurity",
    "cloud",
    "data engineering",
    "iot",
    "blockchain"
]

COMPLEXITY_KEYWORDS = [
    "api",
    "rest api",
    "database",
    "mongodb",
    "sql",
    "authentication",
    "authorization",
    "docker",
    "microservices",
    "fastapi",
    "machine learning",
    "deployment",
    "cloud"
]

IMPACT_KEYWORDS = [
    "automation",
    "prediction",
    "recommendation",
    "optimization",
    "analytics",
    "monitoring",
    "collaboration",
    "detection",
    "tracking",
    "matching",
    "scoring",
    "classification"
]
def calculate_project_impact(readme_text):

    text = readme_text.lower()

    domain_score = 0
    complexity_score = 0
    impact_score = 0

    for keyword in DOMAIN_KEYWORDS:

        if keyword in text:
            domain_score += 5

    for keyword in COMPLEXITY_KEYWORDS:

        if keyword in text:
            complexity_score += 3

    for keyword in IMPACT_KEYWORDS:

        if keyword in text:
            impact_score += 3

    domain_score = min(domain_score, 40)

    complexity_score = min(
        complexity_score,
        30
    )

    impact_score = min(
        impact_score,
        30
    )

    total_score = (
        domain_score
        +
        complexity_score
        +
        impact_score
    )

    return {
        "domain_score": domain_score,
        "complexity_score": complexity_score,
        "impact_score": impact_score,
        "total_score": total_score
    }
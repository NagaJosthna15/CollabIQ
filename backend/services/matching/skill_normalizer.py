import re


def normalize_skill(skill):
    """
    Converts different representations of the same
    skill into a common normalized form.
    """

    if not skill:
        return ""

    skill = str(skill).strip().lower()

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    aliases = {

        # Python
        "python programming": "python",
        "python 3": "python",
        "python development": "python",

        # JavaScript
        "javascript programming": "javascript",
        "js": "javascript",

        # React
        "reactjs": "react",
        "react.js": "react",

        # Node
        "node.js": "nodejs",
        "node js": "nodejs",

        # MongoDB
        "mongo db": "mongodb",

        # Machine Learning
        "machine-learning": "machine learning",
        "machinelearning": "machine learning",
        "ml": "machine learning",

        # HTML
        "html5": "html",

        # CSS
        "css3": "css",

        # SQL
        "sql database": "sql",

        # NLP
        "natural language processing": "nlp",

        # AI
        "artificial intelligence": "ai",

        # REST
        "restful api": "rest api",
        "rest api design": "rest api",
        "restful api design": "rest api",

        # CI/CD
        "ci/cd pipelines": "ci/cd",
        "ci cd": "ci/cd",

        # GitHub Actions
        "github action": "github actions",

        # Hugging Face
        "huggingface": "hugging face",
        "hugging face transformers": "transformers",

        # Scikit Learn
        "scikit learn": "scikit-learn",
        "sklearn": "scikit-learn"

    }

    return aliases.get(
        skill,
        skill
    )


def normalize_skill_list(skills):
    """
    Normalizes a list of skills.
    """

    normalized = set()

    if not skills:
        return normalized

    for skill in skills:

        if not skill:
            continue

        normalized_skill = normalize_skill(
            skill
        )

        if normalized_skill:

            normalized.add(
                normalized_skill
            )

    return normalized


def expand_skill(skill):
    """
    Expands compound or grouped skill requirements.

    Examples:

    Python (Flask/FastAPI/Django)
    ->
    ["python", "flask", "fastapi", "django"]

    Machine Learning frameworks
    (TensorFlow, PyTorch, scikit-learn)
    ->
    [
        "machine learning",
        "tensorflow",
        "pytorch",
        "scikit-learn"
    ]
    """

    if not skill:
        return []

    skill = str(skill).strip().lower()

   

    html_css_patterns = [

        "html/css",
        "html / css",
        "html & css",
        "html and css"

    ]

    if skill in html_css_patterns:

        return [
            "html",
            "css"
        ]


   
    if (
        "python" in skill
        and (
            "flask" in skill
            or "fastapi" in skill
            or "django" in skill
        )
    ):

        return [
            "python",
            "flask",
            "fastapi",
            "django"
        ]


 

    if (
        "machine learning" in skill
        and (
            "tensorflow" in skill
            or "pytorch" in skill
            or "scikit" in skill
        )
    ):

        return [
            "machine learning",
            "tensorflow",
            "pytorch",
            "scikit-learn"
        ]


    if (
        "nlp" in skill
        and (
            "spacy" in skill
            or "hugging face" in skill
            or "transformers" in skill
        )
    ):

        return [
            "nlp",
            "spacy",
            "transformers"
        ]


  
    if (
        "restful api" in skill
        or "rest api" in skill
    ):

        return [
            "rest api"
        ]


    

    if "docker" in skill:

        return [
            "docker"
        ]


  

    if "kubernetes" in skill:

        return [
            "kubernetes"
        ]


   

    if (
        "ci/cd" in skill
        or "ci cd" in skill
        or "github actions" in skill
        or "gitlab ci" in skill
    ):

        return [
            "ci/cd",
            "github actions",
            "gitlab ci"
        ]


   

    if (
        "aws" in skill
        or "azure" in skill
        or "gcp" in skill
    ):

        expanded = []

        if "aws" in skill:
            expanded.append("aws")

        if "azure" in skill:
            expanded.append("azure")

        if "gcp" in skill:
            expanded.append("gcp")

        return expanded


  
    if (
        "oauth2" in skill
        or "jwt" in skill
    ):

        expanded = []

        if "oauth2" in skill:
            expanded.append("oauth2")

        if "jwt" in skill:
            expanded.append("jwt")

        return expanded


   

    match = re.match(
        r"^(.*?)\s*\((.*?)\)$",
        skill
    )

    if match:

        main_skill = match.group(1).strip()

        inner_skills = match.group(2)

        parts = re.split(
            r"[,/]",
            inner_skills
        )

        expanded = []

        if main_skill:

            expanded.append(
                normalize_skill(main_skill)
            )

        for part in parts:

            normalized_part = normalize_skill(
                part.strip()
            )

            if normalized_part:

                expanded.append(
                    normalized_part
                )

        return list(
            dict.fromkeys(expanded)
        )


   
    return [
        normalize_skill(skill)
    ]
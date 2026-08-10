def normalize_skill(skill):
    """
    Converts different representations of the same
    skill into a common normalized form.
    """

    skill = skill.strip().lower()



    aliases = {
        "python programming": "python",
        "python 3": "python",
        "python development": "python",

        "javascript": "javascript",
        "javascript programming": "javascript",
        "js": "javascript",

        "reactjs": "react",
        "react.js": "react",

        "node.js": "nodejs",
        "node js": "nodejs",

        "mongodb": "mongodb",
        "mongo db": "mongodb",

        "machine-learning": "machine learning",
        "machinelearning": "machine learning",

        "html5": "html",

        "css3": "css",

        "sql database": "sql",

        "natural language processing": "nlp",

        "artificial intelligence": "ai"
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

    for skill in skills:

        normalized_skill = normalize_skill(
            skill
        )

        normalized.add(
            normalized_skill
        )

    return normalized


def expand_skill(skill):
    """
    Handles compound skills such as HTML/CSS.
    """

    skill = skill.strip().lower()

    if skill in [
        "html/css",
        "html / css",
        "html & css",
        "html and css"
    ]:
        return [
            "html",
            "css"
        ]

    return [
        normalize_skill(skill)
    ]
def calculate_github_relevance(
    repositories,
    required_skills
):

    score = 0

    for skill in required_skills:

        skill = skill.lower()

        for repo in repositories:

            repo_name = (
                repo.get("name") or ""
            ).lower()

            repo_description = (
                repo.get("description") or ""
            ).lower()

            repo_language = (
                repo.get("language") or ""
            ).lower()

            if (
                skill in repo_name
                or skill in repo_description
                or skill in repo_language
            ):
                score += 20
                break

    return min(score, 100)
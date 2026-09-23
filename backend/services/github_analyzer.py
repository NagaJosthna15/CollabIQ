import requests

GITHUB_API_TIMEOUT = 10


def get_github_profile(username):
    if not username or not str(username).strip():
        return None

    username = str(username).strip()

    url = f"https://api.github.com/users/{username}"

    try:
        response = requests.get(
            url,
            timeout=GITHUB_API_TIMEOUT
        )
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    try:
        user_data = response.json()
    except ValueError:
        return None

    public_repos = user_data.get(
        "public_repos",
        0
    )

    login = user_data.get(
        "login"
    )

    if not login:
        return None

    repos_url = f"https://api.github.com/users/{username}/repos"

    languages = set()

    try:
        repos_response = requests.get(
            repos_url,
            timeout=GITHUB_API_TIMEOUT
        )
    except requests.RequestException:
        repos_response = None

    if repos_response is not None:
        if repos_response.status_code == 200:
            try:
                repos = repos_response.json()
            except ValueError:
                repos = []

            if isinstance(repos, list):
                for repo in repos:
                    if not isinstance(repo, dict):
                        continue

                    language = repo.get(
                        "language"
                    )

                    if language:
                        languages.add(language)

    github_score = min(
        50,
        (public_repos * 2)
        +
        (len(languages) * 5)
    )

    return {
        "username": login,
        "public_repos": public_repos,
        "languages": list(languages),
        "github_score": github_score
    }


def get_github_repositories(username):
    if not username or not str(username).strip():
        return []

    username = str(username).strip()

    repos_url = f"https://api.github.com/users/{username}/repos"

    try:
        response = requests.get(
            repos_url,
            timeout=GITHUB_API_TIMEOUT
        )
    except requests.RequestException:
        return []

    if response.status_code != 200:
        return []

    try:
        repos = response.json()
    except ValueError:
        return []

    if not isinstance(repos, list):
        return []

    repo_list = []

    for repo in repos:
        if not isinstance(repo, dict):
            continue

        repo_list.append({
            "name": repo.get("name"),
            "description": repo.get("description"),
            "language": repo.get("language")
        })

    return repo_list
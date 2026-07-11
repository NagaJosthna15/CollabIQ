import requests

def get_github_profile(username):

    url = f"https://api.github.com/users/{username}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    user_data = response.json()

    repos_url = f"https://api.github.com/users/{username}/repos"

    repos_response = requests.get(repos_url)

    languages = set()

    if repos_response.status_code == 200:

        repos = repos_response.json()

        for repo in repos:

            language = repo.get("language")

            if language:
                languages.add(language)

    github_score = min(
    50,
    (user_data["public_repos"] * 2)
    +
    (len(languages) * 5)
)

    return {
        "username": user_data["login"],
        "public_repos": user_data["public_repos"],
        "languages": list(languages),
        "github_score": github_score
    }
def get_github_repositories(username):

    repos_url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(repos_url)

    if response.status_code != 200:
        return []

    repos = response.json()

    repo_list = []

    for repo in repos:

        repo_list.append({
            "name": repo["name"],
            "description": repo["description"],
            "language": repo["language"],
            
        })

    return repo_list
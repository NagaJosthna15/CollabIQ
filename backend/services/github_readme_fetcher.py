import requests


def get_readme(
    username,
    repo_name
):

    url = f"https://raw.githubusercontent.com/{username}/{repo_name}/main/README.md"

    response = requests.get(url)

    if response.status_code == 200:
        return response.text

    return None
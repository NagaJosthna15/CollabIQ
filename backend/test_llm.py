from services.llm.llm_project_analyzer import analyze_project_with_llm
from services.github_readme_fetcher import (
    get_readme
)

from services.llm.llm_project_analyzer import(
     analyze_project_with_llm
)


readme = get_readme(
    "NagaJosthna15",
    "CodeWave"
)

result = analyze_project_with_llm(
    readme
)

print(result)
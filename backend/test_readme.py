from services.github_readme_fetcher import (
    get_readme
)

from services.project_intelligence import (
    analyze_project
)

readme = get_readme(
    "NagaJosthna15",
    "CodeWave"
)

report = analyze_project(
    readme
)

print(report)
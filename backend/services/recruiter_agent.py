from services.llm.llm_requirement_analyzer import (
    analyze_project_requirements
)


class RecruiterAgent:

    def understand_project(
        self,
        title,
        description
    ):

        requirements = analyze_project_requirements(
            title,
            description
        )

        return requirements
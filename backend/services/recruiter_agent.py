from services.llm.llm_requirement_analyzer import (
    analyze_project_requirements
)

from services.student_service import (
    get_all_students
)

from services.student_profile_builder import (
    StudentProfileBuilder
)

from services.matching.candidate_search import (
    filter_candidates
)

from services.ranking.candidate_ranker import (
    rank_candidates
)

from services.team_builder.team_builder import (
    build_team
)


class RecruiterAgent:

    def __init__(self):
        # Store student profiles here
        self.student_profiles = []


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


    def build_student_profiles(self):

        students = get_all_students()

        builder = StudentProfileBuilder()

        profiles = builder.build_profiles(
            students
        )

        # IMPORTANT:
        # Save profiles so they can be accessed later
        self.student_profiles = profiles

        return profiles


    def recruit_team(
        self,
        title,
        description
    ):

        requirements = self.understand_project(
            title,
            description
        )

        student_profiles = self.build_student_profiles()

        candidates = self.search_candidates(
            requirements,
            student_profiles
        )

        ranked_candidates = rank_candidates(
            requirements,
            candidates
        )

        team_result = build_team(
            requirements,
            ranked_candidates
        )

        return {

            "project_requirements":
                requirements,

            "final_team":
                team_result[
                    "final_team"
                ],

            "coverage":
                team_result[
                    "coverage"
                ],

            "skill_gaps":
                team_result[
                    "skill_gaps"
                ]
        }


    def search_candidates(
        self,
        project_requirements,
        student_profiles
    ):

        candidates = filter_candidates(
            project_requirements,
            student_profiles
        )

        return candidates
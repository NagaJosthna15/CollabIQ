
from services.llm.llm_requirement_analyzer import (
    analyze_project_requirements
)

from services.student_service import get_all_students

from services.student_profile_builder import StudentProfileBuilder

from services.matching.candidate_search import filter_candidates

from services.ranking.candidate_ranker import rank_candidates

from services.team_builder.team_builder import build_team


class RecruiterAgent:

    def __init__(self):
        self.student_profiles = []

    def understand_project(self, title, description):
        requirements = analyze_project_requirements(
            title,
            description
        )
        return requirements

    def build_student_profiles(self):
        students = get_all_students()

        builder = StudentProfileBuilder()
        profiles = builder.build_profiles(students)

        self.student_profiles = profiles
        return profiles

    def search_candidates(self, requirements, student_profiles):
        return filter_candidates(
            requirements,
            student_profiles
        )

    def recruit_team(self, title, description, team_size):
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
            ranked_candidates,
            team_size=team_size
        )

        return {
            "project_requirements": requirements,
            "final_team": team_result["final_team"],
            "coverage": team_result["coverage"],
            "skill_gaps": team_result["skill_gaps"],
            "additional_candidates": team_result.get(
                "additional_candidates", []
            ),
            "additional_candidate_result": team_result.get(
                "additional_candidate_result", {}
            )
        }

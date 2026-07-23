from services.llm.llm_requirement_analyzer import (
    analyze_project_requirements
)
from services.student_service import get_all_students
from services.student_profile_builder import StudentProfileBuilder


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
    def build_student_profiles(self):
        students = get_all_students()

        builder = StudentProfileBuilder()

        profiles = builder.build_profiles(students)

        return profiles
    def recruit_team(self, title, description):
        requirements = self.understand_project(
        title,
        description
    )

        student_profiles = self.build_student_profiles()
        return {
            "project_requirements": requirements,
            "student_profiles": student_profiles
    }
    
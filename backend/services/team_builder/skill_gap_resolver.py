from services.matching.semantic_role_matcher import (
    skill_similarity
)

from services.matching.skill_normalizer import (
    normalize_skill,
    expand_skill
)


SKILL_GAP_THRESHOLD = 0.70


class SkillGapResolver:

    """
    Finds candidates outside the currently selected team
    who may be able to cover missing project skills.
    """

    def find_candidates(
        self,
        missing_skills,
        all_students,
        selected_team
    ):

        # --------------------------------
        # Selected student names
        # --------------------------------

        selected_students = set()

        for member in selected_team:

            student_name = (
                member["candidate"]
                ["profile"]
                ["student"]
            )

            selected_students.add(
                student_name
            )

        # --------------------------------
        # Result
        # --------------------------------

        recommendations = []

        # --------------------------------
        # Check every missing skill
        # --------------------------------

        for missing_skill in missing_skills:

            best_candidates = []

            required_parts = expand_skill(
                missing_skill
            )

            for student in all_students:

                student_name = student.get(
                    "student"
                )

                # Don't recommend already selected
                if student_name in selected_students:
                    continue

                student_skills = []

                student_skills.extend(
                    student.get(
                        "skills",
                        []
                    )
                )

                student_skills.extend(
                    student.get(
                        "resume_skills",
                        []
                    )
                )

                best_similarity = 0

                best_matched_skill = None

                # --------------------------------
                # Compare required skill
                # with student's skills
                # --------------------------------

                for required_part in required_parts:

                    required_part = normalize_skill(
                        required_part
                    )

                    for student_skill in student_skills:

                        similarity = skill_similarity(
                            required_part,
                            student_skill
                        )

                        if similarity > best_similarity:

                            best_similarity = similarity

                            best_matched_skill = (
                                student_skill
                            )

                # --------------------------------
                # Candidate qualifies
                # --------------------------------

                if (
                    best_similarity
                    >= SKILL_GAP_THRESHOLD
                ):

                    best_candidates.append({

                        "student":
                            student_name,

                        "matched_skill":
                            best_matched_skill,

                        "similarity":
                            round(
                                best_similarity,
                                2
                            )

                    })

            # --------------------------------
            # Sort candidates
            # --------------------------------

            best_candidates.sort(
                key=lambda x: x[
                    "similarity"
                ],
                reverse=True
            )

            # --------------------------------
            # Store recommendation
            # --------------------------------

            recommendations.append({

                "missing_skill":
                    missing_skill,

                "candidates":
                    best_candidates

            })

        return recommendations
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

    It also determines whether a missing skill is:
    1. Available in the candidate pool
    2. A genuine skill gap
    """

    def find_candidates(
        self,
        missing_skills,
        all_students,
        selected_team
    ):


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

      

        recommendations = []

     

        for missing_skill in missing_skills:

            candidates = []

         

            required_parts = expand_skill(
                missing_skill
            )

           

            for student in all_students:

                student_name = student.get(
                    "student"
                )

               

                if (
                    student_name
                    in selected_students
                ):

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

              

                student_skills = list(
                    set(student_skills)
                )

                best_similarity = 0

                best_matched_skill = None

                for required_part in required_parts:

                    normalized_required_skill = (
                        normalize_skill(
                            required_part
                        )
                    )

                    for student_skill in student_skills:

                       
                        normalized_student_skill = (
                            normalize_skill(
                                student_skill
                            )
                        )

                        if (
                            normalized_required_skill
                            == normalized_student_skill
                        ):

                            similarity = 1.0

                        else:


                            similarity = skill_similarity(
                                normalized_required_skill,
                                student_skill
                            )
                        if (
                            similarity
                            > best_similarity
                        ):

                            best_similarity = (
                                similarity
                            )

                            best_matched_skill = (
                                student_skill
                            )

                if (
                    best_matched_skill
                    is not None
                    and best_similarity
                    >= SKILL_GAP_THRESHOLD
                ):

                    candidates.append({

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


            candidates.sort(
                key=lambda candidate:
                    candidate["similarity"],
                reverse=True
            )


            if candidates:

                best_candidate = (
                    candidates[0]
                )

                status = (
                    "candidate_available"
                )

                recommendation = (
                    "Consider adding "
                    + best_candidate["student"]
                    + " to improve coverage "
                    + "of "
                    + missing_skill
                    + "."
                )

            else:

                best_candidate = None

                status = (
                    "genuine_skill_gap"
                )

                recommendation = (
                    "No suitable candidate "
                    "with sufficient similarity "
                    "was found. Consider "
                    "upskilling an existing "
                    "team member or recruiting "
                    "an NLP-skilled candidate."
                    if missing_skill.lower()
                    in ["nlp", "nlp techniques"]
                    else
                    "Consider upskilling an "
                    "existing team member or "
                    "recruiting a candidate "
                    "with this skill."
                )

           

            recommendations.append({

                "missing_skill":
                    missing_skill,

                "status":
                    status,

                "best_candidate":
                    best_candidate,

                "candidates":
                    candidates,

                "recommendation":
                    recommendation,

                "is_genuine_gap":
                    not bool(candidates)

            })

    

        return recommendations
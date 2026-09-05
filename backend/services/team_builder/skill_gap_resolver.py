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

    def get_selected_student_name(self, member):

        """
        Safely extract student name from a team member.
        """

        if not isinstance(member, dict):
            return None

        candidate = member.get(
            "candidate",
            {}
        )

        if isinstance(candidate, dict):

            profile = candidate.get(
                "profile",
                {}
            )

            if isinstance(profile, dict):

                student_name = profile.get(
                    "student"
                )

                if student_name:
                    return student_name

        student_name = member.get(
            "student_name"
        )

        if student_name:
            return student_name

        student_name = member.get(
            "student"
        )

        if student_name:
            return student_name

        return None


    def get_student_skills(self, student):

        """
        Collect skills from all possible student fields.
        """

        if not isinstance(student, dict):
            return []

        skills = []

        primary_skills = student.get(
            "skills",
            []
        )

        if isinstance(primary_skills, list):

            skills.extend(
                primary_skills
            )

        resume_skills = student.get(
            "resume_skills",
            []
        )

        if isinstance(resume_skills, list):

            skills.extend(
                resume_skills
            )

        profile_skills = student.get(
            "candidate_skills",
            []
        )

        if isinstance(profile_skills, list):

            skills.extend(
                profile_skills
            )

        unique_skills = []

        seen_skills = set()

        for skill in skills:

            if not skill:
                continue

            normalized = normalize_skill(
                str(skill)
            )

            if (
                normalized
                and normalized not in seen_skills
            ):

                seen_skills.add(
                    normalized
                )

                unique_skills.append(
                    skill
                )

        return unique_skills


    def find_candidates(
        self,
        missing_skills,
        all_students,
        selected_team
    ):

        """
        Find students outside the current team who can
        potentially cover each missing skill.
        """

        # ====================================================
        # BUILD SET OF ALREADY SELECTED STUDENTS
        # ====================================================

        selected_students = set()

        for member in selected_team or []:

            student_name = (
                self.get_selected_student_name(
                    member
                )
            )

            if student_name:

                selected_students.add(
                    str(student_name).lower().strip()
                )


        # ====================================================
        # STORE FINAL RECOMMENDATIONS
        # ====================================================

        recommendations = []


        # ====================================================
        # PROCESS EACH MISSING SKILL
        # ====================================================

        for missing_skill in missing_skills or []:

            candidates = []


            # ------------------------------------------------
            # EXPAND REQUIRED SKILL
            # ------------------------------------------------

            required_parts = expand_skill(
                missing_skill
            )

            if not required_parts:

                required_parts = [
                    missing_skill
                ]


            # ------------------------------------------------
            # CHECK EVERY AVAILABLE STUDENT
            # ------------------------------------------------

            for student in all_students or []:

                if not isinstance(student, dict):
                    continue


                student_name = student.get(
                    "student"
                )

                if not student_name:
                    continue


                normalized_student_name = (
                    str(student_name)
                    .lower()
                    .strip()
                )


                # Skip students already in team

                if (
                    normalized_student_name
                    in selected_students
                ):
                    continue


                # Get all student skills

                student_skills = (
                    self.get_student_skills(
                        student
                    )
                )


                if not student_skills:
                    continue


                best_similarity = 0.0

                best_matched_skill = None


                # --------------------------------------------
                # MATCH REQUIRED SKILL AGAINST STUDENT SKILLS
                # --------------------------------------------

                for required_part in required_parts:

                    normalized_required_skill = (
                        normalize_skill(
                            str(required_part)
                        )
                    )


                    if not normalized_required_skill:
                        continue


                    for student_skill in student_skills:

                        normalized_student_skill = (
                            normalize_skill(
                                str(student_skill)
                            )
                        )


                        if not normalized_student_skill:
                            continue


                        # Exact match

                        if (
                            normalized_required_skill
                            == normalized_student_skill
                        ):

                            similarity = 1.0


                        # Semantic match

                        else:

                            similarity = skill_similarity(
                                normalized_required_skill,
                                normalized_student_skill
                            )


                        # Update best match

                        if (
                            similarity
                            > best_similarity
                        ):

                            best_similarity = similarity

                            best_matched_skill = (
                                student_skill
                            )


                # --------------------------------------------
                # ADD STUDENT IF MATCH IS GOOD ENOUGH
                # --------------------------------------------

                if (
                    best_matched_skill is not None
                    and best_similarity
                    >= SKILL_GAP_THRESHOLD
                ):

                    candidates.append({

                        "student": student_name,

                        "matched_skill":
                            best_matched_skill,

                        "similarity":
                            round(
                                best_similarity,
                                2
                            )

                    })


            # ====================================================
            # SORT CANDIDATES
            # ====================================================

            candidates.sort(

                key=lambda candidate:
                    candidate.get(
                        "similarity",
                        0
                    ),

                reverse=True
            )


            # ====================================================
            # DETERMINE GAP STATUS
            # ====================================================

            if candidates:


                # --------------------------------------------
                # CANDIDATE AVAILABLE
                # --------------------------------------------

                best_candidate = candidates[0]

                status = (
                    "candidate_available"
                )


                candidate_name = (
                    best_candidate.get(
                        "student"
                    )
                    or "the selected candidate"
                )


                missing_skill_text = (
                    str(missing_skill)
                    if missing_skill is not None
                    else "this skill"
                )


                recommendation = (

                    "Consider adding "
                    + str(candidate_name)
                    + " to improve coverage of "
                    + missing_skill_text
                    + "."
                )


            else:


                # --------------------------------------------
                # GENUINE SKILL GAP
                # --------------------------------------------

                best_candidate = None

                status = (
                    "genuine_skill_gap"
                )


                missing_skill_text = (
                    str(missing_skill)
                    if missing_skill is not None
                    else ""
                )


                if (
                    missing_skill_text.lower()
                    in [
                        "nlp",
                        "nlp techniques"
                    ]
                ):

                    recommendation = (

                        "No suitable candidate with "
                        "sufficient similarity was found. "
                        "Consider upskilling an existing "
                        "team member or recruiting an "
                        "NLP-skilled candidate."
                    )


                else:

                    recommendation = (

                        "No suitable candidate with "
                        "sufficient similarity was found. "
                        "Consider upskilling an existing "
                        "team member or recruiting a "
                        "candidate with this skill."
                    )


            # ====================================================
            # SAVE RESULT FOR CURRENT SKILL
            # ====================================================

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


        # ====================================================
        # RETURN ALL GAP RECOMMENDATIONS
        # ====================================================

        return recommendations
def filter_candidates(
    project_requirements,
    student_profiles
):
    """
    Filters students who are relevant
    to the project requirements.
    """

    candidates = []

    return candidates
def filter_candidates(project_requirements, student_profiles):

    # Get required skills from project
    required_skills = project_requirements.get("required_skills", [])

    # Convert project skills to lowercase
    required_skills = [
        skill.lower()
        for skill in required_skills
    ]

    candidates = []

    # Check every student
    for profile in student_profiles:

        skills = profile.get("skills", [])
        resume_skills = profile.get("resume_skills", [])

        # Combine all student skills
        student_skills = skills + resume_skills

        # Convert student skills to lowercase
        student_skills = [
            skill.lower()
            for skill in student_skills
        ]

        matches = 0

        # Compare project skills with student skills
        for required_skill in required_skills:

            for student_skill in student_skills:

                if (
                    required_skill in student_skill
                    or student_skill in required_skill
                ):
                    matches += 1
                    break

        # If at least one skill matches,
        # add student to candidate list
        if matches > 0:
            candidates.append(profile)

    return candidates
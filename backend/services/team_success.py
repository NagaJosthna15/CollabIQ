def calculate_team_success(team):
    if not team:
        return {
            "success_score": 0,
            "success_probability": "Low",
            "skill_coverage": 0,
            "role_balance": 0,
            "team_compatibility": 0,
            "risk_level": "High",
            "risks": ["No team members available"],
            "recommendations": ["Build a team with suitable candidates"]
        }

    scores = []
    roles = []
    skills = set()

    for member in team:
        score = member.get("score")

        if score is None:
            score = member.get("selection_score", 0)

        if isinstance(score, (int, float)):
            scores.append(score)

        role = member.get("role")

        if role:
            roles.append(role)

        candidate = member.get("candidate", {})
        profile = candidate.get("profile", {})

        for skill in profile.get("skills", []):
            skills.add(str(skill).lower())

        for skill in profile.get("resume_skills", []):
            skills.add(str(skill).lower())

    average_score = (
        sum(scores) / len(scores)
        if scores
        else 0
    )

    success_score = round(
        min(average_score, 100),
        2
    )

    unique_roles = len(set(roles))

    if team:
        role_balance = round(
            min(
                (unique_roles / len(team)) * 100,
                100
            ),
            2
        )
    else:
        role_balance = 0

    if len(team) > 1:
        team_compatibility = round(
            min(
                70 + (len(skills) * 2),
                100
            ),
            2
        )
    else:
        team_compatibility = 50

    skill_coverage = round(
        min(
            (len(skills) / max(len(team) * 3, 1)) * 100,
            100
        ),
        2
    )

    if success_score >= 80:
        probability = "High"
    elif success_score >= 60:
        probability = "Medium"
    else:
        probability = "Low"

    risks = []
    recommendations = []

    if skill_coverage < 60:
        risks.append("Team has limited skill coverage")
        recommendations.append(
            "Add candidates with complementary technical skills"
        )

    if role_balance < 60:
        risks.append("Team has limited role diversity")
        recommendations.append(
            "Assign members to complementary roles"
        )

    if team_compatibility < 70:
        risks.append("Team compatibility may be limited")
        recommendations.append(
            "Select members with complementary skills"
        )

    if success_score < 60:
        risks.append("Overall team capability score is low")
        recommendations.append(
            "Consider replacing low-scoring candidates"
        )

    if not risks:
        risk_level = "Low"
    elif len(risks) <= 2:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "success_score": success_score,
        "success_probability": probability,
        "skill_coverage": skill_coverage,
        "role_balance": role_balance,
        "team_compatibility": team_compatibility,
        "risk_level": risk_level,
        "risks": risks,
        "recommendations": recommendations
    }
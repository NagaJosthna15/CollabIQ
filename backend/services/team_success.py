def calculate_team_success(team):

    if not team:
        return {
            "success_score": 0
        }

    total_score = 0

    for member in team:

        total_score += member.get(
            "score",
            0
        )

    average_score = (
        total_score /
        len(team)
    )

    success_score = round(
        average_score,
        2
    )

    if success_score >= 80:
        probability = "High"

    elif success_score >= 60:
        probability = "Medium"

    else:
        probability = "Low"

    return {
        "success_score":
        success_score,

        "success_probability":
        probability
    }
def create_team(matches, team_size):

    sorted_matches = sorted(
        matches,
        key=lambda x: x["match_score"],
        reverse=True
    )

    return sorted_matches[:team_size]
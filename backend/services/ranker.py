def calculate_final_score(
    match_score,
    talent_score
):

    final_score = (
        (match_score * 0.7)
        +
        (talent_score * 0.3)
    )

    return round(final_score, 2)
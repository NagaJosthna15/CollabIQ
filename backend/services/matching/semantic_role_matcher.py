from sentence_transformers import (
    SentenceTransformer,
    util
)


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def text_similarity(
    text_a,
    text_b
):

    embedding_a = model.encode(
        text_a,
        convert_to_tensor=True
    )

    embedding_b = model.encode(
        text_b,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        embedding_a,
        embedding_b
    )

    return round(
        similarity.item(),
        2
    )


def role_similarity(
    recruiter_role,
    candidate_role
):

    return text_similarity(
        recruiter_role,
        candidate_role
    )


def skill_similarity(
    required_skill,
    candidate_skill
):

    return text_similarity(
        required_skill,
        candidate_skill
    )
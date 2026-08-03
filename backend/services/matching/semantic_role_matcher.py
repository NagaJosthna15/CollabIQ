from sentence_transformers import (
    SentenceTransformer,
    util
)
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
def role_similarity(
    recruiter_role,
    candidate_role
):

    recruiter_embedding = model.encode(
        recruiter_role,
        convert_to_tensor=True
    )

    candidate_embedding = model.encode(
        candidate_role,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        recruiter_embedding,
        candidate_embedding
    )
    return round(similarity.item(), 2)

    
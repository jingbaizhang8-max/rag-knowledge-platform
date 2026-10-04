from sentence_transformers import CrossEncoder

Model_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
_model = None

def get_reranker():
    global  _model

    if _model is None:
        _model = CrossEncoder(Model_NAME)

    return  _model


def rerank_chunks(
        query: str,
        candidates: list[dict],
        limit: int = 3
) -> list[dict]:

    if not candidates:
        return []

    pairs = [
        (query, candidate["chunk"]["text"])
        for candidate in candidates
    ]

    model = get_reranker()
    scores = model.predict(pairs)

    reranked = []

    for candidate, score in zip(candidates, scores):
        result = candidate.copy()
        result["rerank_score"] = float(score)
        reranked.append(result)

    reranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return  reranked[:limit]
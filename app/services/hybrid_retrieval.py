from app.services.keyword_retrieval import KeywordRetriever
from app.services.retrieval_service import retrieve_chunks
from app.services.vector_store import get_all_chunks

RRF_K = 60

def hybrid_retrieve(
        query: str,
        limit: int = 3,
        candidate_limit: int = 10,
        document_id: str | None = None
) -> list[dict]:

    vector_results = retrieve_chunks(
        query=query,
        limit=candidate_limit,
        document_id=document_id
    )

    chunks = get_all_chunks()

    if document_id is not None:
        chunks = [
            chunk for chunk in chunks
            if chunk["document_id"] == document_id
        ]

    if chunks:
        keyword_retriever = KeywordRetriever(chunks)
        keyword_results = keyword_retriever.search(
            query=query,
            limit=candidate_limit
        )
    else:
        keyword_results = []

    fused = {}

    for rank, chunk in enumerate(vector_results, start=1):
        key = (
            chunk["document_id"],
            chunk["chunk_index"]
        )

        fused[key] = {
            "chunk": chunk,
            "rrf_score": 1 / (RRF_K + rank),
            "vector_rank": rank,
            "bm25_rank": None
        }

    for rank, result in enumerate(keyword_results, start=1):
        chunk = result["chunk"]

        key = (
            chunk["document_id"],
            chunk["chunk_index"]
        )

        rrf_score = 1 / (RRF_K + rank)

        if key in fused:
            fused[key]["rrf_score"] += rrf_score
            fused[key]["bm25_rank"] = rank

        else:
            fused[key] = {
                "chunk": chunk,
                "rrf_score": rrf_score,
                "vector_rank": None,
                "bm25_rank": rank
            }


    ranked_results = sorted(
        fused.values(),
        key=lambda x: x["rrf_score"],
        reverse=True
    )

    return  ranked_results[:limit]
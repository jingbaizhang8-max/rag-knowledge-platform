from app.services.generation_service import generate_answer
from app.services.hybrid_retrieval import hybrid_retrieve
from app.services.reranker_service import rerank_chunks
from app.services.evidence_verifier import has_sufficient_evidence

RETRIEVAL_THRESHOLD = 0.5

HYBRID_CANDIDATE_LIMIT = 10

RERANK_THRESHOLD = -2.0

def ask_question(
        query: str,
        limit: int = 3,
        document_id: str | None = None
):

    candidates = hybrid_retrieve(
        query=query,
        limit=HYBRID_CANDIDATE_LIMIT,
        candidate_limit=HYBRID_CANDIDATE_LIMIT,
        document_id=document_id
    )

    reranked_results = rerank_chunks(
        query=query,
        candidates=candidates,
        limit=HYBRID_CANDIDATE_LIMIT
    )

    relevant_results = [
        result for result in reranked_results
        if result["rerank_score"] >= RERANK_THRESHOLD
    ][:limit]


    if not relevant_results:
        return {
            "answer": "I don't know based on the provided context.",
            "sources": [],
            "retrieved_chunks": []
        }


    context = "\n\n".join(
        result["chunk"]["text"]
        for result in relevant_results
    )

    has_evidence = has_sufficient_evidence(
        query=query,
        context=context
    )

    if not has_evidence:
        return {
            "answer": "I don't know based on the provided context.",
            "sources": [],
            "retrieved_chunks": []
        }

    answer = generate_answer(
        query=query,
        context=context
    )

    sources = []
    for result in relevant_results:
         chunk = result["chunk"]

         source_info = {
             "source": chunk["source"],
             "page": chunk["page"]
         }

         if source_info not in sources:
             sources.append(source_info)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": relevant_results
    }
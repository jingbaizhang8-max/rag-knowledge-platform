from app.services.generation_service import generate_answer
from app.services.retrieval_service import retrieve_chunks


RETRIEVAL_THRESHOLD = 0.5

def ask_question(
        query: str,
        limit: int = 3
) ->dict:

    retrieved_chunks=retrieve_chunks(
        query=query,
        limit=limit
    )

    relevant_chunks = []

    for chunk in retrieved_chunks:
        if chunk["score"] >= RETRIEVAL_THRESHOLD:
            relevant_chunks.append(chunk)

    if not relevant_chunks:
        return {
            "answer": "I don't know based on the provided context.",
            "sources": [],
            "retrieved_chunks": []
        }

    context_parts = []

    for chunk in relevant_chunks:
        context_parts.append(chunk["text"])

    context = "\n\n".join(context_parts)

    answer = generate_answer(
        query=query,
        context=context
    )

    sources = []
    for chunk in relevant_chunks:
         source_info = {
             "source": chunk["source"],
             "page": chunk["page"]
         }

         if source_info not in sources:
             sources.append(source_info)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": relevant_chunks
    }
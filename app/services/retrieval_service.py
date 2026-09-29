from app.services.embedding_service import embed_query
from app.services.vector_store import search_chunks


def retrieve_chunks(
        query: str,
        limit: int = 3
) -> list[dict]:

    query_vector = embed_query(query)

    results = search_chunks(
        query_vector=query_vector,
        limit=limit
    )

    return results

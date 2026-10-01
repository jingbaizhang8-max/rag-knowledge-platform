from uuid import uuid4

from qdrant_client import QdrantClient, models

COLLECTION_NAME = "knowledge_chunks"
VECTOR_SIZE = 384

qdrant_client = QdrantClient(path="data/qdrant")

def ensure_collection():
    collections = qdrant_client.get_collections().collections

    collection_names = [
        collection.name for collection in collections
    ]

    if COLLECTION_NAME not in collection_names:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )


def store_chunks(
        chunks: list[dict],
        embeddings: list[list[float]]
) -> int:
    ensure_collection()

    points = []
    for chunk, embedding in zip(chunks, embeddings):
        point = models.PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "document_id": chunk["document_id"],
                "chunk_index": chunk["chunk_index"],
                "source": chunk["source"],
                "page": chunk["page"],
                "text": chunk["text"]

            }

        )

        points.append(point)

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return len(points)


def search_chunks(
    query_vector: list[float],
    limit: int = 3,
    document_id: str | None = None
) -> list[dict]:

    ensure_collection()

    query_filter = None

    if document_id is not None:
        query_filter = models.Filter(
            must = [
                models.FieldCondition(
                    key="document_id",
                    match=models.MatchValue(
                        value=document_id
                    )
                )
            ]
        )

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=query_filter,
        limit=limit,
        with_payload=True
    ).points

    retrieved_chunks = []

    for result in results:
        retrieved_chunks.append(
            {
                "score": result.score,
                "document_id": result.payload["document_id"],
                "chunk_index": result.payload["chunk_index"],
                "source": result.payload["source"],
                "page": result.payload["page"],
                "text": result.payload["text"]
            }
        )

    return retrieved_chunks



def close_vector_store():
    qdrant_client.close()








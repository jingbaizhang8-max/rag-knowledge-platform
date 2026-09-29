from app.services.embedding_service import embed_query,embed_texts

def test_embed_query_returns_384_dimensions():
    vector = embed_query("what is RAG?")

    assert len(vector) == 384

def test_embed_texts_returns_one_vector_per_text():
    texts=[
        "RAG combines retrieval with generation.",
        "Vector databases store embeddings."
    ]

    vectors = embed_texts(texts)

    assert len(vectors) == 2
    assert len(vectors[0]) == 384
    assert len(vectors[1]) == 384

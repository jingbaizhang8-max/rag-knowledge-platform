from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )
    return embeddings.tolist()

def embed_query(text: str) -> list[float]:
    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()
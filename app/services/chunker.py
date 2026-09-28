def chunk_text(
        text: str,
        chunk_size: int = 120,
        overlap: int = 30
) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start+chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start = end - overlap
    return chunks

def chunk_pages(
        pages: list[dict],
        document_id: str,
        source: str
) -> list[dict]:
    chunk_records = []
    chunk_index = 0
    for page in pages:
        chunks = chunk_text(page["text"])
        for chunk in chunks:
            chunk_record = {
                "document_id": document_id,
                "chunk_index": chunk_index,
                "source": source,
                "page": page["page"],
                "text": chunk
            }

            chunk_records.append(chunk_record)
            chunk_index += 1
    return chunk_records
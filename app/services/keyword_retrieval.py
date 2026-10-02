from rank_bm25 import BM25Okapi

class KeywordRetriever:
    def __init__(self, chunks):
        self.chunks = chunks

        tokenized = [
            chunk["text"].split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized)

    def search(self, query, limit=3):
        tokens = query.split()
        scores = self.bm25.get_scores(tokens)
        results=[]

        for index, score in enumerate(scores):
            if score > 0:
                results.append(
                    {
                        "score": float(score),
                        "chunk": self.chunks[index]
                    }
                )

        results.sort(
            key=lambda x:x["score"],
            reverse=True
        )

        return results[:limit]
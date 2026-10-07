import json
from pathlib import Path


from app.services.retrieval_service import retrieve_chunks
from app.services.hybrid_retrieval import hybrid_retrieve
from app.services.reranker_service import rerank_chunks
from app.services.vector_store import close_vector_store

TOP_K = 3
CANDIDATE_LIMIT = 10

DATASET_PATH = Path(__file__).parent / "evaluation_dataset.json"

def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def calculate_metrics(retrieved_pages, expected_pages):
    first_relevant_rank = None

    for rank, page in enumerate(retrieved_pages,start=1):
        if page in expected_pages:
            first_relevant_rank = rank
            break

    hit = 1 if first_relevant_rank is not None else 0

    reciprocal_rank = (
        1 / first_relevant_rank
        if first_relevant_rank is not None
        else 0
    )

    return hit, reciprocal_rank


def retrieve_dense(question):
    results = retrieve_chunks(
        query=question,
        limit=TOP_K
    )

    return [
        result["page"]
        for result in results
    ]

def retrieve_hybrid(question):
    results = hybrid_retrieve(
        query=question,
        limit=TOP_K,
        candidate_limit=CANDIDATE_LIMIT
    )

    return [
        result["chunk"]["page"]
        for result in results
    ]

def retrieve_hybrid_rerank(question):
    candidates = hybrid_retrieve(
        query=question,
        limit=CANDIDATE_LIMIT,
        candidate_limit=CANDIDATE_LIMIT
    )

    results = rerank_chunks(
        query=question,
        candidates=candidates,
        limit=TOP_K
    )

    return [
        result["chunk"]["page"]
        for result in results
    ]

def evaluate_method(name, retrieval_function, dataset):
    hits = []
    reciprocal_ranks = []

    print(f"\n==== {name} ====")

    for item in dataset:
        if not item["answerable"]:
            continue

        retrieved_pages = retrieval_function(
            item["question"]
        )

        hit, reciprocal_rank = calculate_metrics(
            retrieved_pages,
            item["expected_pages"]
        )

        hits.append(hit)
        reciprocal_ranks.append(reciprocal_rank)

        print(f"\n{item['id']}")
        print("Expected:", item["expected_pages"])
        print("Retrieved:", retrieved_pages)
        print("Hit:", hit)
        print("RR:", reciprocal_rank)

    hit_at_k =sum(hits) / len(hits)
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print(f"\n{name} Results")
    print(f"Hit@{TOP_K}: {hit_at_k:.3f}")
    print(f"MRR: {mrr:.3f}")

    return {
        "hit_at_k": hit_at_k,
        "mrr": mrr
    }

# def evaluate_question(question, expected_pages):
#     candidates = hybrid_retrieve(
#         query=question,
#         limit=CANDIDATE_LIMIT,
#         candidate_limit=CANDIDATE_LIMIT
#     )
#
#     results = rerank_chunks(
#         query=question,
#         candidates=candidates,
#         limit=TOP_K
#     )
#
#     retrieved_pages = [
#         result["chunk"]["page"]
#         for result in results
#     ]
#
#     first_relevant_rank = None
#
#     for rank, page in enumerate(retrieved_pages, start=1):
#         if page in expected_pages:
#             first_relevant_rank = rank
#             break
#
#     hit = 1 if first_relevant_rank is not None else 0
#
#     reciprocal_rank = (
#         1/first_relevant_rank
#         if first_relevant_rank is not None
#         else 0
#     )
#
#     return {
#         "retrieved_pages": retrieved_pages,
#         "hit": hit,
#         "reciprocal_rank": reciprocal_rank
#     }

def main():
    dataset = load_dataset()

    # hits = []
    # reciprocal_ranks = []
    #
    # try:
    #     for item in dataset:
    #         if not item["answerable"]:
    #             continue
    #
    #         result = evaluate_question(
    #             question=item["question"],
    #             expected_pages=item["expected_pages"]
    #         )
    #
    #         hits.append(result["hit"])
    #         reciprocal_ranks.append(
    #             result["reciprocal_rank"]
    #         )
    #
    #         print(f"\n{item['id']}")
    #         print("Question:", item["question"])
    #         print("Expected pages:", item["expected_pages"])
    #         print("Retrieved pages:", result["retrieved_pages"])
    #         print("Hit@3:", result["hit"])
    #         print("Reciprocal Rank:", result["reciprocal_rank"])
    #
    #     hit_at_k = sum(hits) / len(hits)
    #     mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
    #
    #     print("\n==== Retrieval Evaluation ====")
    #     print(f"Hit@{TOP_K}: {hit_at_k:.3f}")
    #     print(f"MRR: {mrr:.3f}")
    #
    # finally:
    #     close_vector_store()

    try:
        dense_metrics = evaluate_method(
            "Dense Only",
            retrieve_dense,
            dataset
        )

        hybrid_metrics = evaluate_method(
            "Hybrid",
            retrieve_hybrid,
            dataset
        )

        rerank_metrics = evaluate_method(
            "Hybrid + Reranker",
            retrieve_hybrid_rerank,
            dataset
        )

        print("\n===== Final Comparison =====")

        print(
            "Dense Only:",
            dense_metrics
        )

        print(
            "Hybrid:",
            hybrid_metrics
        )

        print(
            "Hybrid + Reranker:",
            rerank_metrics
        )

    finally:
        close_vector_store()

if __name__ == "__main__":
    main()

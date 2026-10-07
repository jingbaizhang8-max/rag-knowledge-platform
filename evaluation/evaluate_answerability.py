import json
from pathlib import Path

from app.services.hybrid_retrieval import hybrid_retrieve
from app.services.reranker_service import rerank_chunks
from app.services.evidence_verifier import has_sufficient_evidence
from app.services.vector_store import close_vector_store


CANDIDATE_LIMIT = 10
FINAL_LIMIT = 3
RERANK_THRESHOLD = -2.0

DATASET_PATH = (
    Path(__file__).parent
    / "evaluation_dataset.json"
)


def load_dataset():
    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def predict_answerable(question):

    candidates = hybrid_retrieve(
        query=question,
        limit=CANDIDATE_LIMIT,
        candidate_limit=CANDIDATE_LIMIT
    )

    reranked_results = rerank_chunks(
        query=question,
        candidates=candidates,
        limit=CANDIDATE_LIMIT
    )

    relevant_results = [
        result
        for result in reranked_results
        if result["rerank_score"] >= RERANK_THRESHOLD
    ][:FINAL_LIMIT]

    if not relevant_results:
        return False

    context = "\n\n".join(
        result["chunk"]["text"]
        for result in relevant_results
    )

    return has_sufficient_evidence(
        query=question,
        context=context
    )


def main():
    dataset = load_dataset()

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    try:
        for item in dataset:

            predicted = predict_answerable(
                item["question"]
            )

            expected = item["answerable"]

            if predicted and expected:
                tp += 1

            elif not predicted and not expected:
                tn += 1

            elif predicted and not expected:
                fp += 1

            else:
                fn += 1

            print(f"\n{item['id']}")
            print("Expected:", expected)
            print("Predicted:", predicted)
            print(
                "Correct:",
                predicted == expected
            )

        total = tp + tn + fp + fn
        accuracy = (tp + tn) / total

        print("\n===== Answerability Evaluation =====")
        print(f"Accuracy: {accuracy:.3f}")
        print(
            f"TP={tp} TN={tn} "
            f"FP={fp} FN={fn}"
        )

    finally:
        close_vector_store()


if __name__ == "__main__":
    main()
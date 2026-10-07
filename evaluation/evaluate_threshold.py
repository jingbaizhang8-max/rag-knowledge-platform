import json
from pathlib import Path

from app.services.hybrid_retrieval import hybrid_retrieve
from app.services.reranker_service import rerank_chunks
from app.services.vector_store import close_vector_store

CANDIDATE_LIMIT = 10
THRESHOLDS = [
    -8.0,
    -5.0,
    -3.0,
    -2.0,
    -1.0,
    0.0,
    1.0,
    2.0
]

DATASET_PATH = (
    Path(__file__).parent / "evaluation_dataset.json"
)

def load_dataset():
    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)

def get_top_rerank_score(question):
    candidates = hybrid_retrieve(
        query=question,
        limit=CANDIDATE_LIMIT,
        candidate_limit=CANDIDATE_LIMIT
    )

    results = rerank_chunks(
        query=question,
        candidates=candidates,
        limit=CANDIDATE_LIMIT
    )

    if not results:
        return None

    return results[0]["rerank_score"]

def main():
    dataset = load_dataset()

    evaluation_results = []

    try:
        for item in dataset:
            score = get_top_rerank_score(
                item["question"]
            )

            evaluation_results.append(
                {
                    "id": item["id"],
                    "score": score,
                    "answerable": item["answerable"]
                }
            )

            print(f"\n{item['id']}")
            print("Question:", item["question"])
            print("Top rerank score:",score)
            print(
                "Expected answerable:",
                item["answerable"]
            )

        print("\n==== Threshold Sweep ====")

        for threshold in THRESHOLDS:
            tp = 0
            tn = 0
            fp = 0
            fn = 0

            for result in evaluation_results:
                predicted = (
                        result["score"] is not None
                        and result["score"] >= threshold
                )

                expected = result["answerable"]

                if predicted and expected:
                    tp += 1

                elif not predicted and not expected:
                    tn += 1

                elif predicted and not expected:
                    fp += 1

                elif not predicted and expected:
                    fn += 1

            total = tp + tn + fp + fn
            accuracy = (tp + tn) / total

            print(
                f"Threshold {threshold:>5}: "
                f"Accuracy={accuracy:.3f} "
                f"TP={tp} TN={tn} FP={fp} FN={fn}"
            )

    finally:
        close_vector_store()

    #         predicted_answerable = (
    #             score is not None
    #             and score >= RERANK_THRESHOLD
    #         )
    #
    #         expected_answerable = item["answerable"]
    #
    #         is_correct = (
    #             predicted_answerable == expected_answerable
    #         )
    #
    #         correct += int(is_correct)
    #         total += 1
    #
    #         print(f"\n{item['id']}")
    #         print("Question:", item["question"])
    #         print("Top rerank score:", score)
    #         print(
    #             "Expected answerable:",
    #             expected_answerable
    #         )
    #         print(
    #             "Predicted answerable:",
    #             predicted_answerable
    #         )
    #         print("Correct:", is_correct)
    #
    #     accuracy = correct / total
    #
    #     print("\n===== Threshold Evaluation =====")
    #     print(
    #         "Threshold:",
    #         RERANK_THRESHOLD
    #     )
    #     print(
    #         f"Accuracy: {accuracy:.3f}"
    #     )
    #
    # finally:
    #     close_vector_store()

if __name__ == "__main__":
    main()
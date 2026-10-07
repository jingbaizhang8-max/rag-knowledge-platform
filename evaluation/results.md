# RAG Evaluation Results

## Evaluation Dataset

- Total cases: 14
- Answerable cases: 8
- Unanswerable cases: 6
- Includes:
  - Exact-match questions
  - Paraphrased questions
  - Out-of-domain negatives
  - Hard negatives

---

## Retrieval Evaluation

Top-K: 3

| Method | Hit@3 | MRR |
|---|---:|---:|
| Dense Retrieval | 1.000 | 0.9375 |
| Hybrid Retrieval (Dense + BM25 + RRF) | 1.000 | 1.000 |
| Hybrid + Cross-Encoder Reranker | 1.000 | 1.000 |

### Observation

Hybrid retrieval improved MRR from 0.9375 to 1.000 on the current evaluation set while maintaining Hit@3 = 1.000.

The current evaluation set does not yet show an additional aggregate MRR improvement from reranking because Hybrid Retrieval already ranks all relevant pages first.

---

## Threshold Evaluation

Initial rerank threshold:


0.0
This caused a false negative on a paraphrased but answerable query.

The threshold was changed to **-2.0**.

At threshold -2.0:

- TP = 8
- TN = 5
- FP = 1
- FN = 0
- Accuracy = 0.929

This reduced false negatives while allowing a later evidence-verification stage to handle ambiguous cases.

---

## Evidence Verification

A separate LLM-based Evidence Verifier was added to distinguish between:

- context that is topically relevant
- context that contains sufficient evidence to answer the question

This addressed hard-negative cases where retrieved content was highly related to the topic but did not contain the specific fact requested by the user.

For example, a query asking which of Kotter, ADKAR, and 7S has the highest proven success rate retrieved highly relevant change-management content, but the document contained no evidence about comparative success rates.

The Evidence Verifier correctly rejected this case.

### Final Answerability Results

- TP = 8
- TN = 6
- FP = 0
- FN = 0
- Accuracy = 1.000

The 1.000 accuracy is reported only on the current 14-case evaluation set and should not be interpreted as general 100% system accuracy.

---

## Final RAG Pipeline

Query  
↓  
Dense Retrieval + BM25  
↓  
Reciprocal Rank Fusion  
↓  
Cross-Encoder Reranker  
↓  
Rerank Threshold (-2.0)  
↓  
Evidence Verifier  
↓  
Grounded LLM Generation  
↓  
Answer + Citation

---

## Key Findings

1. Hybrid retrieval improved MRR from **0.9375 to 1.000** compared with dense-only retrieval on the current evaluation set.

2. A rerank threshold of `0.0` caused a false negative on a paraphrased but answerable query.

3. Lowering the threshold to `-2.0` removed that false negative but introduced one false positive on a hard-negative query.

4. The Evidence Verifier removed the remaining false positive without introducing new false negatives.

5. Retrieval relevance alone is not sufficient to determine whether a question is answerable. A retrieved passage can be highly relevant to the topic while still lacking the specific evidence required to answer the question.
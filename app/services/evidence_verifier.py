from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.deepseek_api_key,
    base_url=settings.deepseek_base_url
)


SYSTEM_PROMPT = """
You are an evidence verification assistant.

Your task is NOT to answer the question.

Decide whether the provided context contains enough explicit evidence
to answer the user's question.

Rules:
1. Judge only from the provided context.
2. Do not use outside knowledge.
3. Topic similarity is not enough.
4. The context must contain the specific information required
   to answer the question.
5. Respond with exactly one word:
   YES
   or
   NO
"""


def has_sufficient_evidence(
    query: str,
    context: str
) -> bool:

    if not context.strip():
        return False

    response = client.chat.completions.create(
        model=settings.deepseek_model,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{query}
"""
            }
        ]
    )

    verdict = (
        response
        .choices[0]
        .message
        .content
        .strip()
        .upper()
    )

    return verdict == "YES"
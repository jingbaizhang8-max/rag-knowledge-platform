from openai import OpenAI
from app.core.config import settings

llm_client = OpenAI(
    api_key=settings.deepseek_api_key,
    base_url=settings.deepseek_base_url
)

def generate_answer(
        query: str,
        context:str
) -> str:

    messages = [
        {
            "role": "system",
            "content": """
    You are a question-answering assistant.

    Answer the user's question using ONLY the provided context.

    If the answer cannot be found in the context,
    say: "I don't know based on the provided context."
    """
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

    response = llm_client.chat.completions.create(
        model=settings.deepseek_model,
        messages=messages
    )

    return  response.choices[0].message.content
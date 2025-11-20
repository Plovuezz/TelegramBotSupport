import json

from openai import AsyncOpenAI

from app.config import get_settings
from app.services.knowledge_service import get_knowledge
from app.services.request_function import REQUEST_FUNCTION

settings = get_settings()

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def get_response(query: str) -> str:

    knowledge = get_knowledge(query, max_chunks=4)

    system_prompt = (
        "Ти — асистент служби підтримки.\n"
        "Використовуй ТІЛЬКИ наданий нижче контекст з бази знань.\n"
        "Якщо в контексті немає необхідної інформації, "
        "запропонуй користувачу залишити заявку на консультацію."
    )

    input_ = [
        {"role": "system", "content": system_prompt},
    ]

    if knowledge:
        input_.append(
            {
                "role": "system",
                "content": f"Контекст:\n{knowledge}",
            }
        )
    else:
        input_.append(
            {
                "role": "system",
                "content": "Для цього запиту немає контексту",
            }
        )

    input_.append({"role": "user", "content": query})

    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=input_,
    )

    answer = resp.choices[0].message.content
    return answer or "На жаль, я не зміг сформувати відповідь."


async def parse_request_with_ai(text: str) -> dict:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ти — асистент, який структурує тексти заявок.\n"
                    "Твоя задача — виділити title, description, contact, meta."
                ),
            },
            {"role": "user", "content": text},
        ],
        tools=[REQUEST_FUNCTION],
        tool_choice={
            "type": "function",
            "function": {"name": "create_request"},
        },
    )

    choice = response.choices[0]
    tool_call = choice.message.tool_calls[0]

    if tool_call.function.name != "create_request":
        raise ValueError("AI викликав не ту функцію")

    data = json.loads(tool_call.function.arguments)
    return data

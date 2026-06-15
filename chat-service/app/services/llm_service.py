from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.config import app_settings
from app.models.message import Message


class LLMService:
    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=app_settings.openai_api_key.get_secret_value()
        )

    async def stream(self, history: list[Message]) -> AsyncIterator[str]:
        messages: list[dict[str, str]] = [
            {"role": "system", "content": app_settings.system_prompt}
        ]
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        stream = await self._client.chat.completions.create(
            model=app_settings.llm_model,
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

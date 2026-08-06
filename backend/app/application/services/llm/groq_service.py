from typing import Generator

from groq import Groq

from app.application.services.llm.llm_service import LLMService
from app.core.config import settings


class GroqService(LLMService):
    """
    Groq implementation of the LLM service.
    """

    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = settings.GROQ_MODEL

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Generate a complete answer using the Groq chat API.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()

    def stream_generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> Generator[str, None, None]:
        """
        Stream the answer token-by-token using the Groq API.
        """

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
            stream=True,
        )

        for chunk in stream:
            if (
                chunk.choices
                and chunk.choices[0].delta.content
            ):
                yield chunk.choices[0].delta.content
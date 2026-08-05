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
        Generate an answer using the Groq chat API.
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
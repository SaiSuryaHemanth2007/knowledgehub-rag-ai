from abc import ABC, abstractmethod


class LLMService(ABC):
    """
    Abstract base class for all language model providers.

    Every provider (Groq, Gemini, OpenAI, Azure OpenAI, etc.)
    should implement this interface.
    """

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Generate a response from the language model.

        Args:
            system_prompt: Instructions for the model.
            user_prompt: User question together with retrieved context.

        Returns:
            Generated answer.
        """
        raise NotImplementedError
import time

from google import genai
from google.genai.errors import ClientError

from app.core.config import settings


class EmbeddingService:
    """
    Generates embeddings using Gemini Embedding.
    Automatically handles Gemini free-tier rate limits.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )

        return response.embeddings[0].values

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        Automatically retries when the Gemini free-tier
        rate limit is reached.
        """

        embeddings = []

        total = len(texts)

        index = 0

        while index < total:

            print(f"Embedding {index + 1}/{total}")

            try:

                embedding = self.generate_embedding(
                    texts[index]
                )

                embeddings.append(embedding)

                index += 1

            except ClientError as e:

                error_message = str(e)

                if (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                ):

                    print()
                    print("=" * 60)
                    print("Gemini rate limit reached.")
                    print("Waiting 60 seconds before retrying...")
                    print("=" * 60)
                    print()

                    time.sleep(60)

                    # Retry the same chunk
                    continue

                # Any other error should stop execution
                raise

        return embeddings
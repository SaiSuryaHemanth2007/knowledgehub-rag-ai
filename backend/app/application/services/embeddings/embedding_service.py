import time

from google import genai
from google.genai.errors import ClientError

from app.core.config import settings


class EmbeddingService:
    """
    Generates embeddings using Gemini Embedding API.

    Uses true batch embedding requests to reduce
    API calls and automatically retries on
    Gemini free-tier rate limits.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY,
        )

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts
        in a single Gemini API request.
        """

        while True:

            try:

                response = self.client.models.embed_content(
                    model=settings.EMBEDDING_MODEL,
                    contents=texts,
                )

                return [
                    embedding.values
                    for embedding in response.embeddings
                ]

            except ClientError as e:

                error_message = str(e)

                if (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                ):

                    print()
                    print("=" * 60)
                    print("Gemini rate limit reached.")
                    print("Waiting 60 seconds before retrying batch...")
                    print("=" * 60)
                    print()

                    time.sleep(60)

                    continue

                raise

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        """
        Convenience method for generating a
        single embedding.
        """

        return self.generate_embeddings(
            [text]
        )[0]
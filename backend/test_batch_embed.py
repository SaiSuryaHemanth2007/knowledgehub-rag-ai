from google import genai

from app.core.config import settings

client = genai.Client(api_key=settings.GOOGLE_API_KEY)

texts = [
    "Artificial Intelligence",
    "Machine Learning",
    "KnowledgeHub RAG AI",
]

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts,
)

print("Embeddings returned:", len(response.embeddings))

for i, embedding in enumerate(response.embeddings):
    print(f"Embedding {i + 1}: {len(embedding.values)} dimensions")
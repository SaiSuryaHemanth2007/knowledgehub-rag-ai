from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GOOGLE_API_KEY)

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents="KnowledgeHub RAG AI"
)

embedding = response.embeddings[0].values

print("Embedding generated successfully!")
print(f"Dimensions: {len(embedding)}")
print("First 5 values:")
print(embedding[:5])
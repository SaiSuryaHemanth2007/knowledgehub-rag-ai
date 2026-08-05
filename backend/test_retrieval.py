from app.infrastructure.database.session import SessionLocal
from app.application.services.retrieval.retrieval_service import (
    RetrievalService,
)

db = SessionLocal()

service = RetrievalService(db)

results = service.retrieve(
    question="What is a repeater?",
    limit=5,
)

print(f"Results: {len(results)}\n")

for i, chunk in enumerate(results, start=1):
    print("=" * 60)
    print(f"Result {i}")
    print(f"Document: {chunk.document_id}")
    print(f"Chunk: {chunk.chunk_index}")
    print(chunk.content[:300])
    print()
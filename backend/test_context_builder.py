from app.application.services.rag.context_builder import (
    ContextBuilder,
)
from app.application.services.retrieval.retrieval_service import (
    RetrievalService,
)
from app.infrastructure.database.session import SessionLocal

db = SessionLocal()

retrieval = RetrievalService(db)

chunks = retrieval.retrieve(
    question="What is a repeater?",
    limit=4,
)

builder = ContextBuilder()

context = builder.build(chunks)

print("=" * 70)
print(context)
print("=" * 70)
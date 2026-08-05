from app.application.services.rag.rag_service import (
    RAGService,
)
from app.infrastructure.database.session import (
    SessionLocal,
)

db = SessionLocal()

rag = RAGService(db)

result = rag.ask(
    "What is a repeater?"
)

print("\n")
print("=" * 80)
print("ANSWER")
print("=" * 80)
print(result["answer"])

print("\n")
print("=" * 80)
print("SOURCES")
print("=" * 80)

for source in result["sources"]:
    print(source)
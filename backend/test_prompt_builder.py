from app.application.services.rag.context_builder import (
    ContextBuilder,
)
from app.application.services.rag.prompt_builder import (
    PromptBuilder,
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

context = ContextBuilder().build(chunks)

system_prompt, user_prompt = PromptBuilder().build(
    context=context,
    question="What is a repeater?",
)

print("=" * 80)
print("SYSTEM PROMPT")
print("=" * 80)
print(system_prompt)

print("\n" + "=" * 80)
print("USER PROMPT")
print("=" * 80)
print(user_prompt)
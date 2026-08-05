from app.application.services.document_processing.document_processor import (
    DocumentProcessor,
)
from app.application.services.pipeline.document_processing_pipeline import (
    DocumentProcessingPipeline,
)
from app.application.services.pipeline.embedding_pipeline import (
    EmbeddingPipeline,
)

# -------------------------------
# Step 1: Extract Text
# -------------------------------

processor = DocumentProcessor()

text = processor.extract_text(
    "uploads/e6f7c662-7fe2-4166-b59f-556ae04699bf.pdf"
)

# -------------------------------
# Step 2: Chunk Document
# -------------------------------

document_pipeline = DocumentProcessingPipeline()

chunks = document_pipeline.process(
    document_id=37,
    extracted_text=text,
)

print(f"Chunks Created: {len(chunks)}")

# -------------------------------
# Step 3: Generate Embeddings
# -------------------------------

embedding_pipeline = EmbeddingPipeline(
    batch_size=20,
)

embeddings = embedding_pipeline.process(
    [chunk.content for chunk in chunks]
)

print("\nEmbedding Pipeline Complete!")

print(f"Embeddings Generated: {len(embeddings)}")

print(f"Embedding Dimensions: {len(embeddings[0])}")

print("\nFirst 5 values:")

print(embeddings[0][:5])
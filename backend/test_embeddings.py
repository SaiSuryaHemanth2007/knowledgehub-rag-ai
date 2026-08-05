from app.application.services.document_processing.document_processor import (
    DocumentProcessor,
)
from app.application.services.pipeline.document_processing_pipeline import (
    DocumentProcessingPipeline,
)
from app.application.services.embeddings.embedding_service import (
    EmbeddingService,
)

# Process document
processor = DocumentProcessor()

text = processor.extract_text(
    "uploads/e6f7c662-7fe2-4166-b59f-556ae04699bf.pdf"
)

pipeline = DocumentProcessingPipeline()

chunks = pipeline.process(
    document_id=37,
    extracted_text=text,
)

print(f"Chunks: {len(chunks)}")

# Generate embeddings
embedding_service = EmbeddingService()

print("\nGenerating embeddings...\n")

embeddings = embedding_service.generate_embeddings(
    [chunk.content for chunk in chunks]
)

print("Embedding generation complete!")

print(f"Embeddings: {len(embeddings)}")

print(f"Dimensions: {len(embeddings[0])}")

print("\nFirst 5 values:")

print(embeddings[0][:5])
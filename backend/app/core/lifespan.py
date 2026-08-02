from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()

    logger.info("🚀 Starting KnowledgeHub RAG AI...")

    yield

    logger.info("🛑 Shutting down KnowledgeHub RAG AI...")
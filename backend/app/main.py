from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.api.v1.health import router as health_router
from app.core.config import settings
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting KnowledgeHub RAG AI...")
    yield
    logger.info("Shutting down KnowledgeHub RAG AI...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
)

app.include_router(health_router)
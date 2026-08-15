from fastapi import APIRouter

from app.api.routers.chat import router as chat_router
from app.api.routers.documents import router as documents_router
from app.api.routers.health import router as health_router
from app.api.routers.conversations import (
    router as conversations_router,
)
from app.api.routers.messages import (
    router as messages_router,
)


api_router = APIRouter()


# Health
api_router.include_router(
    health_router
)


# Documents
api_router.include_router(
    documents_router
)


# Chat
api_router.include_router(
    chat_router
)


# Conversations
api_router.include_router(
    conversations_router
)


# Messages
api_router.include_router(
    messages_router
)
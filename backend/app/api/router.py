from fastapi import APIRouter

from app.api.routers.chat import router as chat_router
from app.api.routers.documents import router as documents_router
from app.api.routers.health import router as health_router

api_router = APIRouter()

# Health endpoints
api_router.include_router(health_router)

# Document endpoints
api_router.include_router(documents_router)

# Chat endpoints
api_router.include_router(chat_router)
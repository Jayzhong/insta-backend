from fastapi import APIRouter

from src.interfaces.api.health import health_router
from src.interfaces.api.users import users_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(users_router)

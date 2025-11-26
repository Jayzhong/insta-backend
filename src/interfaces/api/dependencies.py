from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.password_hasher import AbstractPasswordHasher
from src.application.common.token_service import AbstractTokenService
from src.application.health.health_check import HealthCheckUseCase
from src.application.health.health_repository import AbstractHealthRepository
from src.application.users.avatar_storage import AbstractAvatarStorage
from src.application.users.login_user import LoginUserUseCase
from src.application.users.register_user import RegisterUserUseCase
from src.application.users.update_user_profile import UpdateUserProfileUseCase
from src.application.users.user_repository import AbstractUserRepository
from src.infrastructure.persistence.database import AsyncSessionLocal
from src.infrastructure.persistence.repositories.health_repository import (
    DummyHealthRepository,
)
from src.infrastructure.persistence.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from src.infrastructure.services.password import PasslibPasswordHasher
from src.infrastructure.services.jwt import JWTTokenService
from src.infrastructure.services.storage import LocalAvatarStorage


# --- Database Session ---
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# --- Services ---
def get_password_hasher() -> AbstractPasswordHasher:
    return PasslibPasswordHasher()


def get_token_service() -> AbstractTokenService:
    return JWTTokenService()


def get_avatar_storage() -> AbstractAvatarStorage:
    return LocalAvatarStorage()


# --- Repositories ---
def get_health_repository() -> AbstractHealthRepository:
    return DummyHealthRepository()


def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractUserRepository:
    return SQLAlchemyUserRepository(session)


# --- Health Check Use Case ---
def get_health_check_use_case(
    repo: AbstractHealthRepository = Depends(get_health_repository),
) -> HealthCheckUseCase:
    return HealthCheckUseCase(repo)


# --- User Use Cases ---
def get_register_user_use_case(
    repo: AbstractUserRepository = Depends(get_user_repository),
    hasher: AbstractPasswordHasher = Depends(get_password_hasher),
) -> RegisterUserUseCase:
    return RegisterUserUseCase(repo, hasher)


def get_login_user_use_case(
    repo: AbstractUserRepository = Depends(get_user_repository),
    hasher: AbstractPasswordHasher = Depends(get_password_hasher),
    token_service: AbstractTokenService = Depends(get_token_service),
) -> LoginUserUseCase:
    return LoginUserUseCase(repo, hasher, token_service)


def get_update_user_profile_use_case(
    repo: AbstractUserRepository = Depends(get_user_repository),
    storage: AbstractAvatarStorage = Depends(get_avatar_storage),
) -> UpdateUserProfileUseCase:
    return UpdateUserProfileUseCase(repo, storage)
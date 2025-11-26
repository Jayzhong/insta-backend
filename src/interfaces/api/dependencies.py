from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.password_hasher import AbstractPasswordHasher
from src.application.common.token_service import AbstractTokenService
from src.application.health.health_check import HealthCheckUseCase
from src.application.health.health_repository import AbstractHealthRepository
from src.application.users.avatar_storage import AbstractAvatarStorage
from src.application.posts.post_storage import AbstractPostImageStorage
from src.application.posts.use_cases.create_post import CreatePostUseCase
from src.application.posts.use_cases.get_post import GetPostUseCase
from src.application.posts.use_cases.list_posts import ListPostsUseCase
from src.application.follows.use_cases.follow_user import FollowUserUseCase
from src.application.follows.use_cases.unfollow_user import UnfollowUserUseCase
from src.application.follows.use_cases.get_followers import GetFollowersUseCase
from src.application.follows.use_cases.get_following import GetFollowingUseCase
from src.application.users.login_user import LoginUserUseCase
from src.application.users.register_user import RegisterUserUseCase
from src.application.users.update_user_profile import UpdateUserProfileUseCase
from src.application.users.user_repository import AbstractUserRepository
from src.application.posts.post_repository import AbstractPostRepository
from src.infrastructure.persistence.database import AsyncSessionLocal
from src.infrastructure.persistence.repositories.health_repository import (
    DummyHealthRepository,
)
from src.infrastructure.persistence.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from src.infrastructure.persistence.repositories.post_repository import (
    SQLAlchemyPostRepository,
)
from src.infrastructure.persistence.repositories.follow_repository import (
    SQLAlchemyFollowRepository,
)
from src.infrastructure.services.password import PasslibPasswordHasher
from src.infrastructure.services.jwt import JWTTokenService
from src.infrastructure.services.storage import LocalAvatarStorage
from src.infrastructure.services.post_storage import LocalPostImageStorage
from src.application.follows.follow_repository import AbstractFollowRepository


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


def get_post_image_storage() -> AbstractPostImageStorage:
    return LocalPostImageStorage()


# --- Repositories ---
def get_health_repository() -> AbstractHealthRepository:
    return DummyHealthRepository()


def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractUserRepository:
    return SQLAlchemyUserRepository(session)


def get_post_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractPostRepository:
    return SQLAlchemyPostRepository(session)


def get_follow_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractFollowRepository:
    return SQLAlchemyFollowRepository(session)


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


# --- Post Use Cases ---
def get_create_post_use_case(
    repo: AbstractPostRepository = Depends(get_post_repository),
    storage: AbstractPostImageStorage = Depends(get_post_image_storage),
) -> CreatePostUseCase:
    return CreatePostUseCase(repo, storage)


def get_get_post_use_case(
    repo: AbstractPostRepository = Depends(get_post_repository),
) -> GetPostUseCase:
    return GetPostUseCase(repo)


def get_list_posts_use_case(
    repo: AbstractPostRepository = Depends(get_post_repository),
) -> ListPostsUseCase:
    return ListPostsUseCase(repo)


# --- Follow Use Cases ---
def get_follow_user_use_case(
    follow_repo: AbstractFollowRepository = Depends(get_follow_repository),
    user_repo: AbstractUserRepository = Depends(get_user_repository),
) -> FollowUserUseCase:
    return FollowUserUseCase(follow_repo, user_repo)


def get_unfollow_user_use_case(
    follow_repo: AbstractFollowRepository = Depends(get_follow_repository),
    user_repo: AbstractUserRepository = Depends(get_user_repository),
) -> UnfollowUserUseCase:
    return UnfollowUserUseCase(follow_repo, user_repo)


def get_get_followers_use_case(
    follow_repo: AbstractFollowRepository = Depends(get_follow_repository),
    user_repo: AbstractUserRepository = Depends(get_user_repository),
) -> GetFollowersUseCase:
    return GetFollowersUseCase(follow_repo, user_repo)


def get_get_following_use_case(
    follow_repo: AbstractFollowRepository = Depends(get_follow_repository),
    user_repo: AbstractUserRepository = Depends(get_user_repository),
) -> GetFollowingUseCase:
    return GetFollowingUseCase(follow_repo, user_repo)
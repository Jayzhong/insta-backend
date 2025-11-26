from dataclasses import dataclass
from uuid import UUID

from src.application.follows.follow_repository import AbstractFollowRepository
from src.application.users.user_repository import AbstractUserRepository
from src.domain.follows.entity import Follow
from src.domain.follows.exceptions import (
    AlreadyFollowingError,
    SelfFollowError,
)
from src.domain.users.exceptions import UserNotFoundError


@dataclass(frozen=True)
class FollowUserRequest:
    follower_id: UUID
    followed_id: UUID


class FollowUserUseCase:
    """
    Use case for one user following another.
    """

    def __init__(
        self,
        follow_repo: AbstractFollowRepository,
        user_repo: AbstractUserRepository,
    ) -> None:
        self._follow_repo = follow_repo
        self._user_repo = user_repo

    async def execute(self, request: FollowUserRequest) -> None:
        if request.follower_id == request.followed_id:
            raise SelfFollowError()

        target_user = await self._user_repo.get_by_id(request.followed_id)
        if not target_user:
            raise UserNotFoundError()

        if await self._follow_repo.is_following(request.follower_id, request.followed_id):
            raise AlreadyFollowingError()

        new_follow = Follow(
            follower_id=request.follower_id,
            followed_id=request.followed_id,
        )

        await self._follow_repo.add(new_follow)

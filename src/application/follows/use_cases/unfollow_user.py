from dataclasses import dataclass
from uuid import UUID

from src.application.follows.follow_repository import AbstractFollowRepository
from src.application.users.user_repository import AbstractUserRepository
from src.domain.follows.exceptions import NotFollowingError
from src.domain.users.exceptions import UserNotFoundError


@dataclass(frozen=True)
class UnfollowUserRequest:
    follower_id: UUID
    followed_id: UUID


class UnfollowUserUseCase:
    """
    Use case for one user unfollowing another.
    """

    def __init__(
        self,
        follow_repo: AbstractFollowRepository,
        user_repo: AbstractUserRepository,
    ) -> None:
        self._follow_repo = follow_repo
        self._user_repo = user_repo

    async def execute(self, request: UnfollowUserRequest) -> None:
        target_user = await self._user_repo.get_by_id(request.followed_id)
        if not target_user:
            raise UserNotFoundError()

        if not await self._follow_repo.is_following(request.follower_id, request.followed_id):
            raise NotFollowingError()

        await self._follow_repo.remove(
            follower_id=request.follower_id,
            followed_id=request.followed_id,
        )

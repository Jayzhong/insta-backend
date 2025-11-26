from dataclasses import dataclass
from uuid import UUID

from src.application.follows.follow_repository import AbstractFollowRepository
from src.application.users.user_repository import AbstractUserRepository
from src.domain.users.exceptions import UserNotFoundError
from src.domain.users.user import User


@dataclass(frozen=True)
class GetFollowersRequest:
    user_id: UUID


class GetFollowersUseCase:
    """
    Use case to get a list of users who follow a specific user.
    """

    def __init__(
        self,
        follow_repo: AbstractFollowRepository,
        user_repo: AbstractUserRepository,
    ) -> None:
        self._follow_repo = follow_repo
        self._user_repo = user_repo

    async def execute(self, request: GetFollowersRequest) -> list[User]:
        target_user = await self._user_repo.get_by_id(request.user_id)
        if not target_user:
            raise UserNotFoundError()

        return await self._follow_repo.get_followers(request.user_id)

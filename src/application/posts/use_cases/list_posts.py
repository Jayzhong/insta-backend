from dataclasses import dataclass
from uuid import UUID

from src.application.posts.post_repository import AbstractPostRepository
from src.domain.posts.entity import Post


@dataclass(frozen=True)
class ListPostsRequest:
    user_id: UUID


class ListPostsUseCase:
    """
    Use case for listing all posts by a specific user.
    """

    def __init__(self, post_repo: AbstractPostRepository) -> None:
        self._post_repo = post_repo

    async def execute(self, request: ListPostsRequest) -> list[Post]:
        return await self._post_repo.list_by_user(request.user_id)

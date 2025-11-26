from dataclasses import dataclass
from uuid import UUID

from src.application.posts.post_repository import AbstractPostRepository
from src.domain.posts.entity import Post
from src.domain.posts.exceptions import PostNotFound


@dataclass(frozen=True)
class GetPostRequest:
    post_id: UUID


class GetPostUseCase:
    """
    Use case for retrieving a single post by ID.
    """

    def __init__(self, post_repo: AbstractPostRepository) -> None:
        self._post_repo = post_repo

    async def execute(self, request: GetPostRequest) -> Post:
        post = await self._post_repo.get_by_id(request.post_id)
        if not post:
            raise PostNotFound()
        return post

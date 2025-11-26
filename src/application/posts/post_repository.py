from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.posts.entity import Post


class AbstractPostRepository(ABC):
    """
    Abstract interface for a post repository.
    """

    @abstractmethod
    async def add(self, post: Post) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, post_id: UUID) -> Post | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Post]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, post: Post) -> None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, post: Post) -> None:
        raise NotImplementedError

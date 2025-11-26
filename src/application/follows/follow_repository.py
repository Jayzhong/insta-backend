from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.follows.entity import Follow
from src.domain.users.user import User


class AbstractFollowRepository(ABC):
    """
    Abstract interface for a follow repository.
    """

    @abstractmethod
    async def add(self, follow: Follow) -> None:
        """Adds a new follow relationship."""
        raise NotImplementedError

    @abstractmethod
    async def remove(self, follower_id: UUID, followed_id: UUID) -> None:
        """Removes a follow relationship."""
        raise NotImplementedError

    @abstractmethod
    async def get_followers(self, user_id: UUID) -> list[User]:
        """Returns a list of Users who follow the given user_id."""
        raise NotImplementedError

    @abstractmethod
    async def get_following(self, user_id: UUID) -> list[User]:
        """Returns a list of Users that the given user_id follows."""
        raise NotImplementedError

    @abstractmethod
    async def is_following(self, follower_id: UUID, followed_id: UUID) -> bool:
        """Checks if follower_id is following followed_id."""
        raise NotImplementedError

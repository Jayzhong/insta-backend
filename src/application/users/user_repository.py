from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.users.user import User


class AbstractUserRepository(ABC):
    """
    Abstract interface for a user repository.
    """

    @abstractmethod
    async def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError

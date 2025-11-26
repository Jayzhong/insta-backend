from abc import ABC, abstractmethod


class AbstractPasswordHasher(ABC):
    """
    Abstract interface for a password hashing service.
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool:
        raise NotImplementedError

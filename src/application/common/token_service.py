from abc import ABC, abstractmethod
from uuid import UUID


class AbstractTokenService(ABC):
    """
    Abstract interface for a JWT generation and validation service.
    """

    @abstractmethod
    def generate_token(self, user_id: UUID) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_and_extract_user_id(self, token: str) -> UUID:
        raise NotImplementedError

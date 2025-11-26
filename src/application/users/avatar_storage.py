from abc import ABC, abstractmethod
from uuid import UUID


class AbstractAvatarStorage(ABC):
    """
    Abstract interface for storing user avatar files.
    """

    @abstractmethod
    async def save(self, user_id: UUID, file_name: str, file_data: bytes) -> str:
        """
        Saves the file and returns its public URL.
        """
        raise NotImplementedError

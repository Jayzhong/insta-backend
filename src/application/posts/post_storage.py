from abc import ABC, abstractmethod
from uuid import UUID


class AbstractPostImageStorage(ABC):
    """
    Abstract interface for storing post images.
    """

    @abstractmethod
    async def save(self, post_id: UUID, file_name: str, file_data: bytes) -> str:
        """
        Saves a post image and returns the URL/path.

        Args:
            post_id: The ID of the post the image belongs to.
            file_name: The original name of the file.
            file_data: The binary content of the file.

        Returns:
            The public URL or path to the saved image.
        """
        raise NotImplementedError

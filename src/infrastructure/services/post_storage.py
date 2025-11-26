import os
import aiofiles
from pathlib import Path
from uuid import UUID

from src.application.posts.post_storage import AbstractPostImageStorage


class LocalPostImageStorage(AbstractPostImageStorage):
    """
    Concrete implementation of post image storage using the local filesystem.
    """

    def __init__(self, base_path: str = "uploads/posts", base_url: str = "/static/posts") -> None:
        self._base_path = Path(base_path)
        self._base_url = base_url
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        self._base_path.mkdir(parents=True, exist_ok=True)

    async def save(self, post_id: UUID, file_name: str, file_data: bytes) -> str:
        # Generate a unique filename
        extension = Path(file_name).suffix
        unique_filename = f"{post_id}{extension}"
        file_path = self._base_path / unique_filename

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file_data)

        # Return the relative URL (assuming static file serving is set up)
        return f"{self._base_url}/{unique_filename}"

import os
import aiofiles
from uuid import UUID

from src.application.users.avatar_storage import AbstractAvatarStorage

MEDIA_ROOT = "./media"


class LocalAvatarStorage(AbstractAvatarStorage):
    """
    Concrete implementation for storing avatar files locally.
    """

    async def save(self, user_id: UUID, file_name: str, file_data: bytes) -> str:
        # Ensure the user's media directory exists
        user_media_path = os.path.join(MEDIA_ROOT, "avatars", str(user_id))
        os.makedirs(user_media_path, exist_ok=True)

        # Create a unique file path
        file_path = os.path.join(user_media_path, file_name)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file_data)

        # Return a URL path that can be served by the web server
        return f"/media/avatars/{user_id}/{file_name}"

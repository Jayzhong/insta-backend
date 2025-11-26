from dataclasses import dataclass
from uuid import UUID

from src.application.posts.post_repository import AbstractPostRepository
from src.application.posts.post_storage import AbstractPostImageStorage
from src.domain.posts.entity import Post


@dataclass(frozen=True)
class CreatePostRequest:
    user_id: UUID
    image_file_name: str
    image_file_data: bytes
    caption: str | None = None


class CreatePostUseCase:
    """
    Use case for creating a new post.
    """

    def __init__(
        self,
        post_repo: AbstractPostRepository,
        image_storage: AbstractPostImageStorage,
    ) -> None:
        self._post_repo = post_repo
        self._image_storage = image_storage

    async def execute(self, request: CreatePostRequest) -> Post:
        # 1. Create the post entity first to generate an ID
        # (We need the ID for the image filename)
        new_post = Post(
            user_id=request.user_id,
            image_url="",  # Placeholder, updated below
            caption=request.caption,
        )

        # 2. Save the image
        image_url = await self._image_storage.save(
            post_id=new_post.id,
            file_name=request.image_file_name,
            file_data=request.image_file_data,
        )

        # 3. Update post with actual image URL
        new_post.image_url = image_url

        # 4. Persist to DB
        await self._post_repo.add(new_post)

        return new_post

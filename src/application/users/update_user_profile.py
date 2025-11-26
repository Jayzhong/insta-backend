from dataclasses import dataclass
from uuid import UUID

from src.application.users.avatar_storage import AbstractAvatarStorage
from src.application.users.user_repository import AbstractUserRepository
from src.domain.users.exceptions import UserNotFoundError
from src.domain.users.user import User


@dataclass(frozen=True)
class UpdateUserProfileRequest:
    user_id: UUID
    nickname: str | None = None
    avatar_file_name: str | None = None
    avatar_file_data: bytes | None = None
    bio: str | None = None
    is_public: bool | None = None
    should_delete_avatar: bool = False


class UpdateUserProfileUseCase:
    """
    Use case for updating a user's profile.
    """

    def __init__(
        self,
        user_repo: AbstractUserRepository,
        avatar_storage: AbstractAvatarStorage,
    ) -> None:
        self._user_repo = user_repo
        self._avatar_storage = avatar_storage

    async def execute(self, request: UpdateUserProfileRequest) -> User:
        user = await self._user_repo.get_by_id(request.user_id)
        if not user:
            raise UserNotFoundError()

        if request.nickname is not None:
            user.nickname = request.nickname
        if request.bio is not None:
            user.bio = request.bio
        if request.is_public is not None:
            user.is_public = request.is_public

        if request.should_delete_avatar:
            # Revert to default avatar instead of None
            user.avatar_url = f"https://ui-avatars.com/api/?name={user.username}&background=random"
        elif request.avatar_file_data and request.avatar_file_name:
            avatar_url = await self._avatar_storage.save(
                user_id=user.id,
                file_name=request.avatar_file_name,
                file_data=request.avatar_file_data,
            )
            user.avatar_url = avatar_url

        await self._user_repo.save(user)

        return user

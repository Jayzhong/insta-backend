from dataclasses import dataclass

from src.application.common.password_hasher import AbstractPasswordHasher
from src.application.users.user_repository import AbstractUserRepository
from src.domain.users.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from src.domain.users.user import User


@dataclass(frozen=True)
class RegisterUserRequest:
    username: str
    email: str
    password: str


class RegisterUserUseCase:
    """
    Use case for registering a new user.
    """

    def __init__(
        self,
        user_repo: AbstractUserRepository,
        password_hasher: AbstractPasswordHasher,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    async def execute(self, request: RegisterUserRequest) -> User:
        if await self._user_repo.get_by_username(request.username):
            raise UsernameAlreadyExistsError()

        if await self._user_repo.get_by_email(request.email):
            raise EmailAlreadyExistsError()

        hashed_password = self._password_hasher.hash(request.password)

        # Generate default avatar using ui-avatars.com based on username
        default_avatar_url = f"https://ui-avatars.com/api/?name={request.username}&background=random"

        new_user = User(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            avatar_url=default_avatar_url,
        )

        await self._user_repo.add(new_user)

        return new_user

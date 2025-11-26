from dataclasses import dataclass

from src.application.common.password_hasher import AbstractPasswordHasher
from src.application.common.token_service import AbstractTokenService
from src.application.users.user_repository import AbstractUserRepository
from src.domain.users.exceptions import InvalidCredentialsError


@dataclass(frozen=True)
class LoginUserRequest:
    email: str
    password: str


@dataclass(frozen=True)
class LoginUserResponse:
    access_token: str


class LoginUserUseCase:
    """
    Use case for user login.
    """

    def __init__(
        self,
        user_repo: AbstractUserRepository,
        password_hasher: AbstractPasswordHasher,
        token_service: AbstractTokenService,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._token_service = token_service

    async def execute(self, request: LoginUserRequest) -> LoginUserResponse:
        user = await self._user_repo.get_by_email(request.email)
        if not user:
            raise InvalidCredentialsError()

        if not self._password_hasher.verify(request.password, user.hashed_password):
            raise InvalidCredentialsError()

        access_token = self._token_service.generate_token(user.id)

        return LoginUserResponse(access_token=access_token)

        access_token = self._token_service.generate_token(user.id)

        return LoginUserResponse(access_token=access_token)

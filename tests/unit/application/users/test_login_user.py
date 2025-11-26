import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from src.application.users.login_user import (
    LoginUserUseCase,
    LoginUserRequest,
    LoginUserResponse,
)
from src.application.common.password_hasher import AbstractPasswordHasher
from src.application.common.token_service import AbstractTokenService
from src.application.users.user_repository import AbstractUserRepository
from src.domain.users.exceptions import InvalidCredentialsError
from src.domain.users.user import User


@pytest.fixture
def mock_user_repo():
    return AsyncMock(spec=AbstractUserRepository)


@pytest.fixture
def mock_password_hasher():
    return Mock(spec=AbstractPasswordHasher)


@pytest.fixture
def mock_token_service():
    return Mock(spec=AbstractTokenService)


@pytest.fixture
def login_use_case(mock_user_repo, mock_password_hasher, mock_token_service):
    return LoginUserUseCase(mock_user_repo, mock_password_hasher, mock_token_service)


@pytest.mark.asyncio
async def test_login_success(
    login_use_case, mock_user_repo, mock_password_hasher, mock_token_service
):
    # Arrange
    user_id = uuid4()
    request = LoginUserRequest(email="test@example.com", password="password123")
    user = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_secret",
    )
    
    mock_user_repo.get_by_email.return_value = user
    mock_password_hasher.verify.return_value = True
    mock_token_service.generate_token.return_value = "valid_jwt_token"

    # Act
    result = await login_use_case.execute(request)

    # Assert
    assert isinstance(result, LoginUserResponse)
    assert result.access_token == "valid_jwt_token"
    
    mock_password_hasher.verify.assert_called_with("password123", "hashed_secret")
    mock_token_service.generate_token.assert_called_with(user_id)


@pytest.mark.asyncio
async def test_login_user_not_found(login_use_case, mock_user_repo):
    # Arrange
    request = LoginUserRequest(email="unknown@example.com", password="password123")
    mock_user_repo.get_by_email.return_value = None

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await login_use_case.execute(request)


@pytest.mark.asyncio
async def test_login_wrong_password(
    login_use_case, mock_user_repo, mock_password_hasher
):
    # Arrange
    request = LoginUserRequest(email="test@example.com", password="wrongpassword")
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_secret",
    )
    
    mock_user_repo.get_by_email.return_value = user
    mock_password_hasher.verify.return_value = False

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await login_use_case.execute(request)

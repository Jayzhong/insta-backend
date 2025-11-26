import pytest
from unittest.mock import AsyncMock, Mock

from src.application.users.register_user import (
    RegisterUserUseCase,
    RegisterUserRequest,
)
from src.application.common.password_hasher import AbstractPasswordHasher
from src.application.users.user_repository import AbstractUserRepository
from src.domain.users.exceptions import (
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
)
from src.domain.users.user import User


@pytest.fixture
def mock_user_repo():
    return AsyncMock(spec=AbstractUserRepository)


@pytest.fixture
def mock_password_hasher():
    return Mock(spec=AbstractPasswordHasher)


@pytest.fixture
def register_use_case(mock_user_repo, mock_password_hasher):
    return RegisterUserUseCase(mock_user_repo, mock_password_hasher)


@pytest.mark.asyncio
async def test_register_user_success(
    register_use_case, mock_user_repo, mock_password_hasher
):
    # Arrange
    request = RegisterUserRequest(
        username="testuser", email="test@example.com", password="password123"
    )
    mock_user_repo.get_by_username.return_value = None
    mock_user_repo.get_by_email.return_value = None
    mock_password_hasher.hash.return_value = "hashed_secret"

    # Act
    result = await register_use_case.execute(request)

    # Assert
    assert isinstance(result, User)
    assert result.username == "testuser"
    assert result.email == "test@example.com"
    assert result.hashed_password == "hashed_secret"
    
    # Verify repository interactions
    mock_user_repo.add.assert_called_once()
    saved_user = mock_user_repo.add.call_args[0][0]
    assert saved_user.username == "testuser"


@pytest.mark.asyncio
async def test_register_user_username_exists(register_use_case, mock_user_repo):
    # Arrange
    request = RegisterUserRequest(
        username="existinguser", email="test@example.com", password="password123"
    )
    mock_user_repo.get_by_username.return_value = User(
        username="existinguser",
        email="other@example.com",
        hashed_password="hash"
    )

    # Act & Assert
    with pytest.raises(UsernameAlreadyExistsError):
        await register_use_case.execute(request)
    
    mock_user_repo.add.assert_not_called()


@pytest.mark.asyncio
async def test_register_user_email_exists(register_use_case, mock_user_repo):
    # Arrange
    request = RegisterUserRequest(
        username="newuser", email="existing@example.com", password="password123"
    )
    mock_user_repo.get_by_username.return_value = None
    mock_user_repo.get_by_email.return_value = User(
        username="otheruser",
        email="existing@example.com",
        hashed_password="hash"
    )

    # Act & Assert
    with pytest.raises(EmailAlreadyExistsError):
        await register_use_case.execute(request)

    mock_user_repo.add.assert_not_called()

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from src.application.common.token_service import AbstractTokenService
from src.application.users.user_repository import AbstractUserRepository
from src.domain.users.user import User as DomainUser
from src.interfaces.api.dependencies import (
    get_token_service,
    get_user_repository,
)

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token_service: AbstractTokenService = Depends(get_token_service),
    user_repo: AbstractUserRepository = Depends(get_user_repository),
) -> DomainUser:
    """
    Dependency to get the current authenticated user.
    Verifies JWT from the Authorization header and fetches the user from the DB.
    """
    token = credentials.credentials
    try:
        user_id = token_service.verify_and_extract_user_id(token)
        user = await user_repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

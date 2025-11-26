import os
from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt

from src.application.common.token_service import AbstractTokenService
from src.domain.users.exceptions import InvalidCredentialsError

# It's recommended to use environment variables for these
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))


class JWTTokenService(AbstractTokenService):
    """
    Concrete implementation of the token service using python-jose.
    """

    def generate_token(self, user_id: UUID) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode = {"exp": expire, "sub": str(user_id)}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_and_extract_user_id(self, token: str) -> UUID:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise InvalidCredentialsError()
            return UUID(user_id)
        except JWTError:
            raise InvalidCredentialsError()

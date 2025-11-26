from passlib.context import CryptContext

from src.application.common.password_hasher import AbstractPasswordHasher


class PasslibPasswordHasher(AbstractPasswordHasher):
    """
    Concrete implementation of the password hasher using passlib.
    Uses Argon2, which is modern, secure, and handles long passwords natively.
    """

    def __init__(self) -> None:
        self._context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self._context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self._context.verify(password, hashed_password)
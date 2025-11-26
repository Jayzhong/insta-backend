from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(kw_only=True)
class User:
    """
    The User aggregate root entity.
    """
    id: UUID = field(default_factory=uuid4)
    username: str
    email: str
    hashed_password: str
    nickname: str | None = None
    avatar_url: str | None = None
    bio: str | None = None
    is_public: bool = True

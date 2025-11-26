import uuid
from datetime import datetime
from sqlalchemy import UUID, Boolean, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.users.user import User as DomainUser
from src.infrastructure.persistence.database import Base


class SQLAlchemyUser(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(50))
    avatar_url: Mapped[str | None] = mapped_column(String(512))
    bio: Mapped[str | None] = mapped_column(Text)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )


def user_to_domain(user: SQLAlchemyUser) -> DomainUser:
    """Maps an ORM user object to a domain user entity."""
    return DomainUser(
        id=user.id,
        username=user.username,
        email=user.email,
        hashed_password=user.password_hash,
        nickname=user.nickname,
        avatar_url=user.avatar_url,
        bio=user.bio,
        is_public=user.is_public,
    )


def user_to_orm(user: DomainUser) -> SQLAlchemyUser:
    """Maps a domain user entity to an ORM user object."""
    return SQLAlchemyUser(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=user.hashed_password,
        nickname=user.nickname,
        avatar_url=user.avatar_url,
        bio=user.bio,
        is_public=user.is_public,
    )

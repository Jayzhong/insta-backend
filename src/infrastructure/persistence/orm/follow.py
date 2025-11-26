import sqlalchemy as sa
from datetime import datetime
from sqlalchemy import UUID, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.follows.entity import Follow as DomainFollow
from src.infrastructure.persistence.database import Base


class SQLAlchemyFollow(Base):
    __tablename__ = "follows"

    follower_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )
    followed_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    __table_args__ = (
        # Index for getting all followers of a user
        sa.Index("ix_follows_followed_id", "followed_id"),
        # Index for getting all users a specific user follows
        sa.Index("ix_follows_follower_id", "follower_id"),
    )


def follow_to_domain(orm_follow: SQLAlchemyFollow) -> DomainFollow:
    return DomainFollow(
        follower_id=orm_follow.follower_id,
        followed_id=orm_follow.followed_id,
        created_at=orm_follow.created_at,
    )


def follow_to_orm(domain_follow: DomainFollow) -> SQLAlchemyFollow:
    return SQLAlchemyFollow(
        follower_id=domain_follow.follower_id,
        followed_id=domain_follow.followed_id,
        created_at=domain_follow.created_at,
    )

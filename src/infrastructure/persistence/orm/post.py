import uuid
from datetime import datetime
import sqlalchemy as sa # Added import
from sqlalchemy import UUID, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.posts.entity import Post as DomainPost
from src.infrastructure.persistence.database import Base


class SQLAlchemyPost(Base):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    image_url: Mapped[str] = mapped_column(String(512), nullable=False)
    caption: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationship to User (optional, but useful for joins)
    # user = relationship("SQLAlchemyUser", back_populates="posts")

    __table_args__ = (
        # Index for efficient lookup of posts by user
        sa.Index("ix_posts_user_id", "user_id"), # Corrected
        # Index for efficient sorting of posts by creation date
        sa.Index("ix_posts_created_at", "created_at"), # Corrected
    )


def post_to_domain(post: SQLAlchemyPost) -> DomainPost:
    """Maps an ORM post object to a domain post entity."""
    return DomainPost(
        id=post.id,
        user_id=post.user_id,
        image_url=post.image_url,
        caption=post.caption,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


def post_to_orm(post: DomainPost) -> SQLAlchemyPost:
    """Maps a domain post entity to an ORM post object."""
    return SQLAlchemyPost(
        id=post.id,
        user_id=post.user_id,
        image_url=post.image_url,
        caption=post.caption,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )

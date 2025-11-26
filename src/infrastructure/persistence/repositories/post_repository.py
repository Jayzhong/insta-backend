from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.posts.post_repository import AbstractPostRepository
from src.domain.posts.entity import Post as DomainPost
from src.infrastructure.persistence.orm.post import (
    SQLAlchemyPost,
    post_to_domain,
    post_to_orm,
)


class SQLAlchemyPostRepository(AbstractPostRepository):
    """
    Concrete implementation of the post repository using SQLAlchemy.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, post: DomainPost) -> None:
        orm_post = post_to_orm(post)
        self._session.add(orm_post)
        await self._session.commit()

    async def get_by_id(self, post_id: UUID) -> DomainPost | None:
        stmt = select(SQLAlchemyPost).where(SQLAlchemyPost.id == post_id)
        result = await self._session.execute(stmt)
        orm_post = result.scalar_one_or_none()
        return post_to_domain(orm_post) if orm_post else None

    async def list_by_user(self, user_id: UUID) -> list[DomainPost]:
        stmt = (
            select(SQLAlchemyPost)
            .where(SQLAlchemyPost.user_id == user_id)
            .order_by(SQLAlchemyPost.created_at.desc())
        )
        result = await self._session.execute(stmt)
        orm_posts = result.scalars().all()
        return [post_to_domain(p) for p in orm_posts]

    async def delete(self, post: DomainPost) -> None:
        # We can delete by ID directly to avoid attaching the object if not needed,
        # but typically we delete the object itself.
        # Here, we delete based on ID to be safe.
        stmt = delete(SQLAlchemyPost).where(SQLAlchemyPost.id == post.id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def save(self, post: DomainPost) -> None:
        await self._session.merge(post_to_orm(post))
        await self._session.commit()

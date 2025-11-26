from uuid import UUID

from sqlalchemy import select, delete, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.follows.follow_repository import AbstractFollowRepository
from src.domain.follows.entity import Follow as DomainFollow
from src.domain.users.user import User as DomainUser
from src.infrastructure.persistence.orm.follow import (
    SQLAlchemyFollow,
    follow_to_domain,
    follow_to_orm,
)
from src.infrastructure.persistence.orm.user import (
    SQLAlchemyUser,
    user_to_domain,
)


class SQLAlchemyFollowRepository(AbstractFollowRepository):
    """
    Concrete implementation of the follow repository using SQLAlchemy.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, follow: DomainFollow) -> None:
        orm_follow = follow_to_orm(follow)
        self._session.add(orm_follow)
        await self._session.commit()

    async def remove(self, follower_id: UUID, followed_id: UUID) -> None:
        stmt = delete(SQLAlchemyFollow).where(
            SQLAlchemyFollow.follower_id == follower_id,
            SQLAlchemyFollow.followed_id == followed_id,
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_followers(self, user_id: UUID) -> list[DomainUser]:
        # Join Follow -> User (where Follow.followed_id == user_id, select User who is follower)
        stmt = (
            select(SQLAlchemyUser)
            .join(SQLAlchemyFollow, SQLAlchemyFollow.follower_id == SQLAlchemyUser.id)
            .where(SQLAlchemyFollow.followed_id == user_id)
        )
        result = await self._session.execute(stmt)
        orm_users = result.scalars().all()
        return [user_to_domain(u) for u in orm_users]

    async def get_following(self, user_id: UUID) -> list[DomainUser]:
        # Join Follow -> User (where Follow.follower_id == user_id, select User who is followed)
        stmt = (
            select(SQLAlchemyUser)
            .join(SQLAlchemyFollow, SQLAlchemyFollow.followed_id == SQLAlchemyUser.id)
            .where(SQLAlchemyFollow.follower_id == user_id)
        )
        result = await self._session.execute(stmt)
        orm_users = result.scalars().all()
        return [user_to_domain(u) for u in orm_users]

    async def is_following(self, follower_id: UUID, followed_id: UUID) -> bool:
        stmt = select(
            exists().where(
                SQLAlchemyFollow.follower_id == follower_id,
                SQLAlchemyFollow.followed_id == followed_id,
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar() or False

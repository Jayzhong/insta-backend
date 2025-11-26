from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.users.user_repository import AbstractUserRepository
from src.domain.users.user import User as DomainUser
from src.infrastructure.persistence.orm.user import (
    SQLAlchemyUser,
    user_to_domain,
    user_to_orm,
)


class SQLAlchemyUserRepository(AbstractUserRepository):
    """
    Concrete implementation of the user repository using SQLAlchemy.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user: DomainUser) -> None:
        orm_user = user_to_orm(user)
        self._session.add(orm_user)
        await self._session.commit()

    async def get_by_id(self, user_id: UUID) -> DomainUser | None:
        stmt = select(SQLAlchemyUser).where(SQLAlchemyUser.id == user_id)
        result = await self._session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        return user_to_domain(orm_user) if orm_user else None

    async def get_by_username(self, username: str) -> DomainUser | None:
        stmt = select(SQLAlchemyUser).where(SQLAlchemyUser.username == username)
        result = await self._session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        return user_to_domain(orm_user) if orm_user else None

    async def get_by_email(self, email: str) -> DomainUser | None:
        stmt = select(SQLAlchemyUser).where(SQLAlchemyUser.email == email)
        result = await self._session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        return user_to_domain(orm_user) if orm_user else None

    async def save(self, user: DomainUser) -> None:
        # The session tracks changes on attached objects, so a flush is enough.
        # Merging ensures the object is attached to the session.
        await self._session.merge(user_to_orm(user))
        await self._session.commit()

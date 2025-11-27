# repositories/base.py
from typing import TypeVar, Generic, Type, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get(self, id_: int) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == id_)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def list(self) -> Sequence[T]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return res.scalars().all()

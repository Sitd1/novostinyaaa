# app/infrastructure/database/repositories/source.py
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models.source import NewsSourceORM


class SourceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_by_name(
            self,
            name: str,
            type_: str = "telegram",
            title: Optional[str] = None
    ) -> NewsSourceORM:
        """Получить источник по имени или создать новый."""
        # Сначала ищем существующий
        stmt = select(NewsSourceORM).where(NewsSourceORM.name == name)
        result = await self.session.execute(stmt)
        source = result.scalar_one_or_none()

        if source:
            return source

        # Создаем новый источник
        source = NewsSourceORM(
            name=name,
            type=type_,
            title=title or name,  # Если title не указан, используем name
        )
        self.session.add(source)
        await self.session.flush()
        return source
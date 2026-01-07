# news.py (репозиторий)

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from shared.database.models.news import NewsEventORM


class NewsRepository(BaseRepository[NewsEventORM]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, NewsEventORM)

    async def save_many_for_run(self, run_id: int, items: list[dict]) -> List[NewsEventORM]:
        """
        items — dict'ы с полями под News, БЕЗ run_fk.
        Здесь мы сами проставляем run_fk = run_id.
        """
        created: list[NewsEventORM] = []

        for data in items:
            news = NewsEventORM(**data, run_fk=run_id)
            self.session.add(news)
            created.append(news)

        await self.session.flush()
        return created

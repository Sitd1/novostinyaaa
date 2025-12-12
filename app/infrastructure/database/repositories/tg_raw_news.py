from typing import Any, Iterable

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.raw_news import RawNewsORM


class TgRawNewsRepository:
    """
    Простейший репозиторий для сохранения сырых новостей из Telegram.

    Важно:
    - Никаких commit / rollback здесь нет.
      Предполагается, что транзакцией управляет get_session().
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, news: RawNewsORM) -> RawNewsORM:
        """
        Добавить готовый ORM-объект в сессию и сделать flush.
        """
        self.session.add(news)
        await self.session.flush()
        return news

    async def save_one(self, data: dict[str, Any]) -> RawNewsORM:
        """
        Создать TgRawNews из dict и сохранить.

        data должен содержать поля, совместимые с TgRawNews(**data).
        """
        news = RawNewsORM(**data)
        self.session.add(news)
        await self.session.flush()
        return news

    async def save_many(self, items: Iterable[dict[str, Any]]) -> list[RawNewsORM]:
        """
        Массовое сохранение пачки сырых новостей.

        items — iterable из dict'ов, которые подходят для TgRawNews(**data).
        """
        objects: list[RawNewsORM] = []

        for data in items:
            news = RawNewsORM(**data)
            objects.append(news)
            self.session.add(news)

        if objects:
            await self.session.flush()

        return objects

    async def get_last_message_id(self, channel_username: str) -> int | None:
        """
        Вернуть максимальный message_id для данного канала, если он есть.
        Иначе — None.
        """
        stmt = (
            select(func.max(RawNewsORM.external_id))
            .where(RawNewsORM.channel_username == channel_username)
        )
        result = await self.session.execute(stmt)
        last_id: int | None = result.scalar_one_or_none()
        return last_id

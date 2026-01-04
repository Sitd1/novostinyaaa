# app/apps/crawler/run_crawler.py

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_async_session as get_session
from app.infrastructure.crawler.tg_crawler.telegram_raw_news_source import (
    create_telegram_raw_news_source
)
from app.core.application.raw_news.use_cases.ingest import ingest_new_raw_news
from app.core.domain.raw_news.services import RawNewsFactory


async def run_telegram_crawler():
    """
    Запуск краулера Telegram каналов.

    Использует контекстный менеджер для автоматического
    управления жизненным циклом клиента и сессии БД.
    """
    async with get_session() as session:
        # Создать источник новостей с зависимостями
        source = await create_telegram_raw_news_source(session)

        # Создать фабрику для доменных сущностей
        factory = RawNewsFactory()

        # Получить репозиторий (если он не создан в create_telegram_raw_news_source)
        from app.infrastructure.database.repositories.raw_news import RawNewsRepositoryImpl
        repo = RawNewsRepositoryImpl(session)

        # Использовать контекстный менеджер для управления клиентом
        async with source:
            print("🚀 Начинаю сбор новостей из Telegram каналов...")

            # Запустить основной use-case
            count = await ingest_new_raw_news(
                source=source,
                factory=factory,
                repo=repo
            )

            print(f"✅ Собрано и сохранено новостей: {count}")

            # Зафиксировать транзакцию
            await session.commit()


async def run_telegram_crawler_alternative():
    """
    Альтернативный вариант с явным управлением клиентом.
    Используйте этот подход, если нужен больший контроль.
    """
    async with get_session() as session:
        source = await create_telegram_raw_news_source(session)
        factory = RawNewsFactory()

        from app.infrastructure.database.repositories.raw_news import RawNewsRepositoryImpl
        repo = RawNewsRepositoryImpl(session)

        try:
            # Явно запустить клиент
            await source.client.start()

            print("🚀 Начинаю сбор новостей из Telegram каналов...")
            count = await ingest_new_raw_news(source, factory, repo)
            print(f"✅ Собрано и сохранено новостей: {count}")

            await session.commit()

        finally:
            # Явно остановить клиент
            await source.client.disconnect()


if __name__ == "__main__":
    # Запустить краулер
    asyncio.run(run_telegram_crawler())
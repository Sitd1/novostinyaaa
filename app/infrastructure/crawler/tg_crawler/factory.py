from telethon import TelegramClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import crawler_config as config
from app.infrastructure.crawler.tg_crawler.raw_news_source import TelegramRawNewsSource
from app.infrastructure.database.repositories.tg_raw_news import TgRawNewsRepository


async def create_telegram_raw_news_source(session: AsyncSession) -> TelegramRawNewsSource:
    """
    Фабрика для создания TelegramRawNewsSource с зависимостями.
    """
    # Создать Telegram клиент
    client = TelegramClient(
        config.telegram.session_name,
        int(config.telegram.api_id.get_secret_value()),
        config.telegram.api_hash.get_secret_value(),
    )

    # Создать репозиторий
    repo = TgRawNewsRepository(session)

    # Создать и вернуть источник
    return TelegramRawNewsSource(
        client=client,
        repo=repo,
        limit_per_channel=50  # можно вынести в конфиг
    )

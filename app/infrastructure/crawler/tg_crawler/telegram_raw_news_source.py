from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.crawler.tg_crawler.raw_news_source import TelegramRawNewsSource
from app.infrastructure.database.repositories.tg_raw_news import TgRawNewsRepository
from app.infrastructure.crawler.tg_crawler.client import get_telegram_client


async def create_telegram_raw_news_source(session: AsyncSession) -> TelegramRawNewsSource:
    """
    Фабрика для создания TelegramRawNewsSource с зависимостями.
    """
    # Создать Telegram клиент
    client = get_telegram_client()

    # Создать репозиторий
    repo = TgRawNewsRepository(session)

    # Создать и вернуть источник
    return TelegramRawNewsSource(
        client=client,
        repo=repo,
        limit_per_channel=50  # можно вынести в конфиг
    )


if __name__ == "__main__":
    from app.infrastructure.database.session import AsyncSession
    source = create_telegram_raw_news_source(AsyncSession)

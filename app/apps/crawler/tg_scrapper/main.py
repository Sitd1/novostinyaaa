from app.infrastructure.database.async_connection.session import get_session
from app.infrastructure.crawler.tg_crawler.factory import create_telegram_raw_news_source
from app.core.application.raw_news.use_cases.ingest import ingest_new_raw_news


# + фабрика RawNewsFactory и репозиторий RawNewsRepository


async def main():
    async with get_session() as session:
        # Создать источник данных из Telegram
        source = await create_telegram_raw_news_source(session)  # штука, которая работает через Telethon

        # Создать фабрику и репозиторий (нужно реализовать)
        factory = ...  # просто штука, которая преобразовывает сообщения из телеграм в доменные сущности
        repo = ...  # RawNewsRepository просто реализовать боевой

        # Запустить клиента и выполнить сбор
        async with source.client:  # клиент должен быть запущен
            count = await ingest_new_raw_news(
                source=source,
                factory=factory,  # будет реализовано позже
                repo=repo  # будет реализовано позже
            )

        print(f"Собрано {count} новых сообщений")


# ToDo реализовываем то, что описано выше и пробуем запуститься

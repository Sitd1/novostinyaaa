# agents_service/telegram_raw/probe_collect.py
import asyncio
from typing import Any

from database.async_connection.session import get_session
from shared.database.repositories.raw_news import RawNewsRepository  # ToDo - создать репозиторий
from apps.crawler.services.tg_crawler.client import get_telegram_client
from apps.crawler.services.tg_crawler.tg_channels import TG_CHANNELS


async def collect_last_messages(limit_per_channel: int = 50) -> None:
    """
    Пробный запуск:
    - проходимся по списку каналов
    - смотрим, какой последний message_id по каждому каналу уже есть в БД
    - берём только сообщения с id > last_message_id
    - сохраняем их в TgRawNews
    """
    client = get_telegram_client()
    await client.start()

    async with client:
        async with get_session() as session:
            repo = RawNewsRepository(session)

            total_saved = 0

            for channel in TG_CHANNELS:
                print(f"\nЧитаю канал: {channel}") # ToDo переделать под логгер

                # 1. узнаём максимальный message_id для этого канала в БД
                last_id = await repo.get_last_message_id(channel)
                print(f"Последний сохранённый message_id для {channel}: {last_id}")

                # 2. собираем только новые сообщения
                new_items: list[dict[str, Any]] = []

                iter_kwargs: dict[str, Any] = {"limit": limit_per_channel}
                if last_id is not None:
                    # Telethon вернёт только сообщения с id > min_id
                    iter_kwargs["min_id"] = last_id

                async for msg in client.iter_messages(channel, **iter_kwargs):
                    if not msg.message:
                        continue

                    data: dict[str, Any] = {
                        "channel_username": channel,
                        "message_id": msg.id,
                        "date": msg.date,
                        "text": msg.message,
                    }
                    new_items.append(data)

                if not new_items:
                    print(f"Новых сообщений для {channel} нет.")
                    continue

                saved = await repo.save_many(new_items)
                print(
                    f"Для канала {channel} сохранено новых сообщений: {len(saved)}"
                )
                total_saved += len(saved)

            print(f"\nИтого сохранено сообщений: {total_saved}")


if __name__ == "__main__":
    asyncio.run(collect_last_messages(limit_per_channel=50))

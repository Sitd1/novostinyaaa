import asyncio
from typing import Any

from shared.database.async_connection.session import get_session
from shared.database.repositories.source import SourceRepository
from shared.database.repositories.raw_news import RawNewsRepository
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
            source_repo = SourceRepository(session)

            total_saved = 0

            for channel in TG_CHANNELS:
                print(f"\nЧитаю канал: {channel}")

                # 1. Получаем или создаем источник
                source = await source_repo.get_or_create_by_name(
                    name=channel,
                    type_="telegram",
                    title=channel  # Пока используем имя канала как title
                )
                print(f"Источник: {source.name} (id={source.id})")

                # 2. узнаём максимальный external_id для этого источника в БД
                last_id = await repo.get_last_external_id(source.id)
                print(f"Последний сохранённый external_id для {channel}: {last_id}")

                # 3. собираем только новые сообщения
                new_items: list[dict[str, Any]] = []

                iter_kwargs: dict[str, Any] = {"limit": limit_per_channel}
                if last_id is not None:
                    # Telethon вернёт только сообщения с id > min_id
                    iter_kwargs["min_id"] = int(last_id)

                async for msg in client.iter_messages(channel, **iter_kwargs):
                    if not msg.message:
                        continue

                    data: dict[str, Any] = {
                        "source_fk": source.id,  # Используем ID источника вместо channel_username
                        "external_id": str(msg.id),  # message_id как строка
                        "published_at": msg.date,  # Корректное название поля
                        "text": msg.message,
                        "importance": 0,  # Default importance for raw news (will be calculated later)
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

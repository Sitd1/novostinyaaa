from typing import Iterable, AsyncIterator
from telethon import TelegramClient
from telethon.tl.types import Message

from app.core.application.raw_news.dto.external_raw_news_item import ExternalRawNewsItem
from app.core.application.raw_news.ports.ingest import ExternalRawNewsSource
from app.infrastructure.database.repositories.tg_raw_news import TgRawNewsRepository
from app.apps.scraper.tg_scrapper.tg_channels import TG_CHANNELS


class TelegramRawNewsSource(ExternalRawNewsSource):
    """
    Адаптер для получения сырых новостей из Telegram каналов.

    Реализует порт ExternalRawNewsSource для архитектуры Clean Architecture.
    """

    def __init__(
            self,
            client: TelegramClient,
            repo: TgRawNewsRepository,
            channels: list[str] = None,
            limit_per_channel: int = 50  # ToDo: вынести в конфиг
    ):
        self.client = client
        self.repo = repo
        self.channels = channels or TG_CHANNELS
        self.limit_per_channel = limit_per_channel

    async def fetch_new_raw_items(self) -> Iterable[ExternalRawNewsItem]:
        """
        Получить новые сырые новости из всех настроенных каналов.

        Для каждого канала:
        1. Определяет последний сохранённый message_id
        2. Получает только сообщения новее этого ID
        3. Преобразует в ExternalRawNewsItem
        """
        for channel in self.channels:
            async for item in self._fetch_channel_items(channel):
                yield item

    async def _fetch_channel_items(self, channel: str) -> AsyncIterator[ExternalRawNewsItem]:
        """
        Получить новые сообщения из конкретного канала.
        """
        # 1. Получить последний сохранённый message_id для канала
        last_id = await self.repo.get_last_message_id(channel)

        # 2. Настроить параметры для iter_messages
        iter_kwargs = {"limit": self.limit_per_channel}
        if last_id is not None:
            # Telethon вернёт только сообщения с id > min_id
            iter_kwargs["min_id"] = last_id

        # 3. Получить новые сообщения
        async for message in self.client.iter_messages(channel, **iter_kwargs):
            if not message.message:  # Пропустить сообщения без текста
                continue

            # 4. Преобразовать в ExternalRawNewsItem
            item = self._message_to_external_item(message, channel)
            yield item

    def _message_to_external_item(self, message: Message, channel: str) -> ExternalRawNewsItem:
        """
        Преобразовать Telegram Message в ExternalRawNewsItem.
        """
        return ExternalRawNewsItem(
            external_id=str(message.id),  # message_id как строка
            source=channel,  # имя канала как источник
            text=message.message,  # текст сообщения
            published_at=message.date.isoformat()  # дата в ISO формате
        )

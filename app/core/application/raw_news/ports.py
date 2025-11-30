from typing import Protocol, Iterable
from app.core.application.raw_news.dto.external_raw_news_item import ExternalRawNewsItem


class ExternalRawNewsSource(Protocol):
    """
    Порт для источника сырых новостей (Telegram, RSS, API и т.п.).
    """

    async def fetch_new_raw_items(self) -> Iterable[ExternalRawNewsItem]:
        ...

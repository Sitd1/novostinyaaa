from typing import Protocol, Iterable
from external_raw_news_item import ExternalRawNewsItem


# --- ingest ---
class ExternalRawNewsSource(Protocol):
    """
    Порт для источника сырых новостей (Telegram, RSS, API и т.п.).
    """

    async def fetch_new_raw_items(self) -> Iterable[ExternalRawNewsItem]:
        ...

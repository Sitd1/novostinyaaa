from typing import Protocol, Iterable
from app.core.application.raw_news.dto.external_raw_news_item import ExternalRawNewsItem
from app.core.domain.raw_news.entities import RawNews
from app.core.application.raw_news.dto.raw_news_enrichment_item import RawNewsEnrichmentResult


# --- ingest
class ExternalRawNewsSource(Protocol):
    """
    Порт для источника сырых новостей (Telegram, RSS, API и т.п.).
    """

    async def fetch_new_raw_items(self) -> Iterable[ExternalRawNewsItem]:
        ...


# --- processing
class RawNewsEnrichmentService(Protocol):
    async def enrich(self, item: RawNews) -> RawNewsEnrichmentResult:
        """
        Порт для обогащения сырых новостей данными

        Один вызов:
        - читает RawNews.text (и др. поля)
        - возвращает всё, что нужно разом.
        """
        ...

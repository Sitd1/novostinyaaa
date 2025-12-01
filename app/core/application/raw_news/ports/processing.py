from typing import Protocol
from app.core.application.raw_news.dto.raw_news_enrichment_item import RawNewsEnrichmentResult
from app.core.domain.raw_news.entities import RawNews


# --- processing ---
class RawNewsEnrichmentService(Protocol):
    async def enrich(self, item: RawNews) -> RawNewsEnrichmentResult:
        """
        Порт для обогащения сырых новостей данными

        Один вызов:
        - читает RawNews.text (и др. поля)
        - возвращает всё, что нужно разом.
        """
        ...

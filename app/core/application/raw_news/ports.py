from typing import Protocol, Iterable
from app.core.domain.raw_news.entities import RawNews
# dto
from app.core.application.raw_news.dto.external_raw_news_item import ExternalRawNewsItem
from app.core.application.raw_news.dto.raw_news_enrichment_item import RawNewsEnrichmentResult
from app.core.application.raw_news.dto.find_similarity_raw_news_items import SimilarRawNews, RawNewsCluster


# --- ingest ---
class ExternalRawNewsSource(Protocol):
    """
    Порт для источника сырых новостей (Telegram, RSS, API и т.п.).
    """

    async def fetch_new_raw_items(self) -> Iterable[ExternalRawNewsItem]:
        ...


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


# --- similarity ---

class VectorSearchService(Protocol):
    """
    Порт к векторному поиску (Qdrant, PGVector, что угодно).
    """

    async def find_similar(
        self,
        item: RawNews,
        limit: int = 10,
        score_threshold: float | None = None,
    ) -> list["SimilarRawNews"]:
        ...


class RawNewsClusterRepository(Protocol):
    """
    Репозиторий для кластеров (групп) RawNews.
    """

    async def save_cluster(self, cluster: RawNewsCluster) -> None:
        ...

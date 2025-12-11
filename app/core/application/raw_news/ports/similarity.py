from typing import Protocol

# dto
from app.core.application.raw_news.dto.find_similarity_raw_news_items import SimilarRawNews, RawNewsCluster
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.news.repositories import NewsEventRepository
from config import ClusteringConfig
from entities import NewsEvent


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


class SimilarityMatcherService(Protocol):
    async def match_raw_news_event(
            self, raw_news: RawNews,
            candidates: list[NewsEvent],
            event_repo: NewsEventRepository,
            config: ClusteringConfig
    ) -> NewsEvent: ...

    async def get_similar_news_candidates(
            self,
            raw_news: RawNews,
            candidates: list[NewsEvent],
            config: ClusteringConfig
    ) -> dict[NewsEvent, float]:
        ...

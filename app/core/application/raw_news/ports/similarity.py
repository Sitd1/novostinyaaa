from typing import Protocol

# dto
from app.core.application.raw_news.dto.find_similarity_raw_news_items import SimilarRawNews, RawNewsCluster
from app.core.domain.raw_news.entities import RawNews


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

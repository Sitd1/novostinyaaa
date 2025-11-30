# Шаг 4
# 4. Работа с векторами
#     - Найти похожие raw_news (по embedding)
#     - Объединить похожие raw_news в группы (кластеризация) ---->(как указать группы?)
# Работа с RawNews закончена
from __future__ import annotations


from typing import Iterable
from app.core.domain.raw_news.entities import RawNews

from app.core.application.raw_news.dto.find_similarity_raw_news_items import SimilarRawNews, RawNewsCluster
from app.core.application.raw_news.ports.similarity import VectorSearchService, RawNewsClusterRepository


async def find_similar_raw_news(
    items: Iterable[RawNews],
    vector_search: VectorSearchService,
    limit_per_item: int = 10,
    score_threshold: float | None = None,
) -> dict[int, list[SimilarRawNews]]:
    """
    Use case:
    - для каждого RawNews найти похожие raw_news.
    - вернуть словарь: raw_news.id -> список похожих.
    """
    result: dict[int, list[SimilarRawNews]] = {}

    for item in items:
        similars = await vector_search.find_similar(
            item,
            limit=limit_per_item,
            score_threshold=score_threshold,
        )
        result[item.id] = similars  # предполагаем, что у RawNews есть .id

    return result


async def cluster_raw_news(
    items: Iterable[RawNews],
    vector_search: VectorSearchService,
    cluster_repo: RawNewsClusterRepository,
    min_cluster_size: int = 2,
) -> list[RawNewsCluster]:
    """
    Use case:
    - наивная кластеризация:
      для каждого элемента ищем похожих и собираем простые группы.
    - в реальной жизни сюда можно подставить DBSCAN/HDBSCAN/что-нибудь сложнее,
      но для старта хватит простого варианта.
    """
    # Очень простая (и наивная) стратегия:
    # - берём элемент, находим похожих
    # - если их >= min_cluster_size, создаём кластер.
    clusters: list[RawNewsCluster] = []

    for item in items:
        similars = await vector_search.find_similar(item)
        group = [item] + [s.raw_news for s in similars]
        if len(group) < min_cluster_size:
            continue

        cluster_id = f"raw-news-cluster-{item.id}"
        cluster = RawNewsCluster(id=cluster_id, items=group)
        clusters.append(cluster)
        await cluster_repo.save_cluster(cluster)

    return clusters

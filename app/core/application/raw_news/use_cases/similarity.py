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



from __future__ import annotations

from datetime import timedelta

from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import RawNewsRepository, NewsEventRepository, EmbeddingSimilarityService
from app.core.application.raw_news.config import ClusteringConfig


async def cluster_pending_raw_news(
    raw_repo: RawNewsRepository,
    events_repo: NewsEventRepository,
    similarity_service: EmbeddingSimilarityService,
    config: ClusteringConfig | None = None,
    limit: int | None = None,
) -> None:
    """
    Use case:
    - забрать пачку RawNews, у которых есть embedding, но ещё нет события
    - для каждой найти похожие новости по embedding в окне по времени
    - решить: присоединить к существующему событию или создать новое.
    """
    if config is None:
        config = ClusteringConfig()

    items = await raw_repo.list_pending_for_clustering(limit=limit)

    for raw in items:
        # На всякий случай — пропускаем, если embedding нет (не обработали enrichment)
        if raw.embedding is None:
            continue

        await _assign_single_raw_news_to_event(
            raw=raw,
            raw_repo=raw_repo,
            events_repo=events_repo,
            similarity_service=similarity_service,
            config=config,
        )


async def _assign_single_raw_news_to_event(
    raw: RawNews,
    raw_repo: RawNewsRepository,
    events_repo: NewsEventRepository,
    similarity_service: EmbeddingSimilarityService,
    config: ClusteringConfig,
) -> None:
    """
    Логика для одной RawNews:
    - поиск ближайших соседей по embedding в окне [published_at - delta, published_at + delta]
    - выбор лучшего (по cosine similarity)
    - если best_score >= threshold → присоединяем к его событию
      иначе → создаём новое событие.
    """
    center_ts = raw.published_at.value  # если RawPublishedAt — VO, берём .value (datetime)
    time_from = center_ts - config.time_window
    time_to = center_ts + config.time_window

    candidates = await raw_repo.search_similar_by_embedding(
        embedding=raw.embedding,
        published_from=time_from,
        published_to=time_to,
        top_k=config.top_k_neighbors,
    )

    best_candidate: RawNews | None = None
    best_score: float = -1.0

    for candidate in candidates:
        # можно отфильтровать ту же самую news на всякий случай
        if candidate.id == raw.id:
            continue
        if candidate.embedding is None:
            continue

        score = await similarity_service.cosine_similarity(raw.embedding, candidate.embedding)
        if score > best_score:
            best_score = score
            best_candidate = candidate

    if best_candidate is None or best_score < config.similarity_threshold:
        # Похожих нет → создаём новое событие
        event = await events_repo.create_from_raw_news(raw)
        await raw_repo.attach_to_event(raw, event)
        # bounds у нового события можно проставить сразу в create_from_raw_news
    else:
        # Нашли подходящее событие → присоединяем к нему
        if best_candidate.event_id is None:
            # теоретически не должно быть, но на всякий случай можно обработать
            # например, создать event для best_candidate
            event = await events_repo.create_from_raw_news(best_candidate)
            await raw_repo.attach_to_event(best_candidate, event)
        else:
            event = await events_repo.get_by_id(best_candidate.event_id)

        if event is None:
            # fallback: если по какой-то причине event не нашли — создаём новый
            event = await events_repo.create_from_raw_news(raw)

        await raw_repo.attach_to_event(raw, event)
        await events_repo.update_bounds(event, raw)

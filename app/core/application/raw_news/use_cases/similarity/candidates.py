from __future__ import annotations

from asyncpg.cluster import Cluster

from app.core.application.raw_news.config import ClusteringConfig
from app.core.domain.news.entities import NewsEvent
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import NewsEventRepository, EventMatcherService



async def find_event_candidates_for_raw_news(
        raw_news: RawNews,
        events_repo: NewsEventRepository,
        event_matcher: EventMatcherService,
        config: ClusteringConfig
) -> list[NewsEvent]:
    """Находит и ранжирует кандидатов событий для новости."""

    # 1. Загружаем новости, ожидающие кластеризации (присвоение event для raw_news)
    candidates: list[NewsEvent] = events_repo.get_news_events_candidates(raw_news, config)

    if not candidates:
        return []

    # 2. Находим косинусную близость для каждого кандидата для нашего raw_news
    similarity_scores: dict[NewsEvent, float] = await event_matcher.get_similar_news_candidates(
        raw_news, candidates, config
    )

    # 3. Отфильтровываем по similarity_threshold
    chosen_candidates: list[NewsEvent] = [
        candidate for candidate, similarity_score
        in similarity_scores.items()
        if similarity_score > config.similarity_threshold
    ]
    return chosen_candidates

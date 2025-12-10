from __future__ import annotations

from app.core.application.raw_news.config import ClusteringConfig
from app.core.domain.news.entities import NewsEvent
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import (
    NewsEventRepository,
    SimilarityMatcherService
)


# Use case для выбора лучшего события
async def choose_best_event_for_raw_news(
        raw_news: RawNews,
        similarity_candidates: dict[NewsEvent, float],
        similarity_matcher: SimilarityMatcherService
) -> NewsEvent | None:
    """Выбирает лучшее событие на основе similarity scores."""

    if not similarity_candidates:
        return None

    return await similarity_matcher.choose_event_for_raw_news(
        raw_news, similarity_candidates
    )

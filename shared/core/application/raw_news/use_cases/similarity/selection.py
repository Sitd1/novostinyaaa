from __future__ import annotations

from application import ClusteringConfig
from entities import NewsEvent
from entities import RawNews
from repositories import (
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

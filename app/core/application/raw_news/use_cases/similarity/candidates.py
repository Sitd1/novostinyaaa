from __future__ import annotations

from app.core.application.raw_news.config import ClusteringConfig
from app.core.domain.news.entities import NewsEvent
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import NewsEventRepository, SimilarityMatcherService



async def find_event_candidates_for_raw_news(
        raw_news: RawNews,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig
) -> dict[NewsEvent, float]:
    """Находит и ранжирует кандидатов событий для новости."""

    # Получаем предварительных кандидатов
    candidates = events_repo.get_news_events_candidates(raw_news, config)

    if not candidates:
        return {}

    # Получаем оценки similarity для кандидатов
    similarity_scores = await similarity_matcher.get_similar_news_candidates(
        raw_news, config
    )

    return similarity_scores

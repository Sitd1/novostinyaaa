from __future__ import annotations

from app.core.application.raw_news.config import ClusteringConfig
from app.core.domain.news.entities import NewsEvent
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import (
    RawNewsRepository,
    NewsEventRepository,
    SimilarityMatcherService
)

# Use case для обработки одной новости
async def process_single_raw_news_for_event(
        raw_news: RawNews,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig):
    """
    Обрабатывает одну новость: находит подходящее событие или создаёт новое.
    Возвращает: (обновлённая_новость, новое_событие, обновлённое_событие)
    """
    pass


# Use case для обработки пачки новостей
async def process_raw_news_batch_for_events(
        raw_news: RawNews,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig
):
    pass

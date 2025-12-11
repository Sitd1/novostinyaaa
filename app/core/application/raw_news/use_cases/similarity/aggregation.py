from __future__ import annotations

from app.core.application.raw_news.config import ClusteringConfig
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import (
    RawNewsRepository
)
from app.core.domain.news.repositories import NewsEventRepository
from app.core.application.raw_news.use_cases.similarity import (
    load_pending_raw_news_for_clustering,
    process_raw_news_batch_for_events,
    persist_event_aggregation_results
)
from app.core.application.raw_news.ports.similarity import SimilarityMatcherService
from app.core.application.raw_news.dto.event_agg_result import EventAggregationResult


# главный оркестратор
async def create_events_from_raw_news(
        raw_news_repo: RawNewsRepository,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig,
        batch_size: int = 50
):

    # 1. Загружаем необработанные новости
    raw_news_list: list[RawNews] = await load_pending_raw_news_for_clustering(raw_news_repo, batch_size)

    # 2. Обрабатываем и получаем результаты
    result: EventAggregationResult = await process_raw_news_batch_for_events(
        raw_news_list,
        events_repo,
        similarity_matcher,
        config
    )

    # 3. Сохраняем результаты
    await persist_event_aggregation_results(result, raw_news_repo, events_repo)

    return result

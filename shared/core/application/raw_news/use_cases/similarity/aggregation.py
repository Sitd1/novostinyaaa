from __future__ import annotations

from find_similarity_raw_news_items import ClusteringConfig
from entities import RawNews
from repositories import (
    RawNewsRepository
)
from repositories import NewsEventRepository
from similarity import (
    load_pending_raw_news_for_clustering,
    process_raw_news_batch_for_events,
    persist_event_aggregation_results
)
from similarity import SimilarityMatcherService
from event_agg_result import EventAggregationResult


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

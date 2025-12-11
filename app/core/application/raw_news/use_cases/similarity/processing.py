from __future__ import annotations

from app.core.application.raw_news.dto.event_agg_result import EventAggregationResult
from app.core.application.raw_news.ports.similarity import SimilarityMatcherService
from app.core.application.raw_news.use_cases.similarity.candidates import find_event_candidates_for_raw_news
from app.core.domain.news.entities import NewsEvent
from app.core.domain.news.repositories import NewsEventRepository
from app.core.domain.raw_news.entities import RawNews
from app.core.application.raw_news.dto.find_similarity_raw_news_items import ClusteringConfig


# Use case для обработки одной новости (Вот эту часть можно вывести в сторону агента)
async def process_single_raw_news_for_event(
        raw_news: RawNews,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig) -> tuple[RawNews, NewsEvent]:
    """
    Обрабатывает одну сырую новость: находит подходящее событие или создаёт новое.

    Returns:
        tuple[обновлённая_новость, новое_событие, обновлённое_событие]

        Только одно из последних двух значений будет не None:
        - Если создано новое событие: (обновлённая_новость, новое_событие, None)
        - Если присоединено к существующему: (обновлённая_новость, None, обновлённое_событие)
    """

    # 1. Находим кандидаты на присвоение Event для конкретной новости (raw_news)
    candidates = await find_event_candidates_for_raw_news(
        raw_news=raw_news,
        events_repo=events_repo,
        similarity_matcher=similarity_matcher,
        config=config
    )

    # 2. Определяем итоговый event (может быть как новая или обновленная новость)
    event: NewsEvent = await similarity_matcher.match_raw_news_event(raw_news, candidates, events_repo, config)
    raw_news = raw_news.with_event_key(event.id)

    return raw_news, event


# Use case для обработки пачки новостей
async def process_raw_news_batch_for_events(
        raw_news_list: list[RawNews],
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig
) -> EventAggregationResult:

    updated_raw_news = []
    new_events = []
    updated_events = []

    for raw_news in raw_news_list:
        raw_news_with_event_fk, event_processed = await process_single_raw_news_for_event(
            raw_news=raw_news,
            events_repo=events_repo,
            similarity_matcher=similarity_matcher,

            config=config
        )
        updated_raw_news.append(raw_news_with_event_fk)
        if event_processed.is_updated:
            updated_events.append(event_processed)
        else:
            new_events.append(event_processed)

    return EventAggregationResult(
        updated_raw_news=updated_raw_news,
        new_events=new_events,
        updated_events=updated_events
    )

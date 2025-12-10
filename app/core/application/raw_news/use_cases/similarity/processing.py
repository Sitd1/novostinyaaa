from __future__ import annotations

from app.core.application.raw_news.config import ClusteringConfig
from app.core.domain.news.entities import NewsEvent
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import (
    RawNewsRepository,
    NewsEventRepository,
    SimilarityMatcherService,
    EventMatcherService
)
from app.core.application.raw_news.use_cases.similarity.candidates import find_event_candidates_for_raw_news
from app.core.application.raw_news.dto.event_agg_result import EventAggregationResult

# Use case для обработки одной новости
async def process_single_raw_news_for_event(
        raw_news: RawNews,
        events_repo: NewsEventRepository,
        event_matcher: EventMatcherService,
        config: ClusteringConfig):
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
        event_matcher=event_matcher,
        config=config
    )

    if not candidates:
        new_event = events_repo.new_event(raw_news=raw_news)
        updated_raw = raw_news.with_event_key(new_event.event_key)
        return updated_raw, new_event

    # 2. Пропускаем через "умный оценщик" наших кандидатов (в любом случае будет updated)
    chosen_event = await event_matcher.choose_event_for_raw_news(raw_news=raw_news, candidates=candidates)

    return ...












# Use case для обработки пачки новостей
async def process_raw_news_batch_for_events(
        raw_news_list: list[RawNews],
        events_repo: NewsEventRepository,
        event_matcher: EventMatcherService,
        config: ClusteringConfig
):
    processed_results = []
    for raw_news in raw_news_list:
        res = process_single_raw_news_for_event(
            raw_news=raw_news,
            events_repo=events_repo,
            event_matcher=event_matcher,
            config=config
        )
        processed_results.append(res)
    return processed_results

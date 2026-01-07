from __future__ import annotations


from repositories import RawNewsRepository
from repositories import NewsEventRepository
from event_agg_result import EventAggregationResult


async def persist_event_aggregation_results(
        result: EventAggregationResult,
        raw_repo: RawNewsRepository,
        events_repo: NewsEventRepository
) -> None:
    """
    Сохраняет результаты агрегации событий в репозиториях.

    Сохраняет:
    1. Обновленные сырые новости (с присвоенными event_id)
    2. Новые созданные события
    3. Обновленные существующие события (с присоединенными новостями)
    """

    # Сохраняем обновленные сырые новости
    if result.updated_raw_news:
        await raw_repo.update_many(result.updated_raw_news)

    # Сохраняем новые события
    if result.new_events:
        await events_repo.save_many(result.new_events)

    # Сохраняем обновленные существующие события
    if result.updated_events:
        await events_repo.update_many(result.updated_events)

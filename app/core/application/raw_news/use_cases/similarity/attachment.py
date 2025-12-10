from __future__ import annotations

from app.core.domain.news.entities import NewsEvent
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import NewsEventRepository


# Use case для присоединения к существующему событию
async def attach_raw_news_to_existing_event(
        raw_news: RawNews,
        target_event: NewsEvent,
        events_repo: NewsEventRepository
) -> tuple[RawNews, NewsEvent]:
    """Присоединяет сырую новость к существующему событию."""

    updated_event = await events_repo.attach_raw_to_existing_event(
        raw_news, target_event
    )
    updated_raw = raw_news.with_event_key(updated_event.id)

    return updated_raw, updated_event

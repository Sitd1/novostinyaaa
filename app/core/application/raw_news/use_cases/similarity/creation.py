from __future__ import annotations

from app.core.domain.news.entities import NewsEvent
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import NewsEventRepository



# Use case для создания нового события
async def create_new_event_from_raw_news(
        raw_news: RawNews,
        events_repo: NewsEventRepository
) -> tuple[RawNews, NewsEvent]:
    """Создаёт новое событие из сырой новости."""

    new_event = await events_repo.create_from_raw_news(raw_news)
    updated_raw = raw_news.with_event_key(new_event.id)

    return updated_raw, new_event

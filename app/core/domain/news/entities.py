from datetime import datetime
from dataclasses import dataclass

from app.core.domain.news.value_objects import NewsEventId, Title, Summary, ImportanceLevel, Topic, Tag, Geography, \
    EventTime
from app.core.domain.raw_news.value_objects import RawNewsId


@dataclass(frozen=True)
class NewsEvent:
    id: NewsEventId
    created_at: datetime
    updated_at: datetime

    # связь с сырыми новостями (могут жить в инфраструктуре/ORM)
    raw_news_ids: tuple[RawNewsId]

    title: Title
    summary: Summary
    importance: ImportanceLevel
    topics: tuple[Topic]
    tags: tuple[Tag]
    geography: Geography | None

    event_time: EventTime   # когда это произошло / актуально

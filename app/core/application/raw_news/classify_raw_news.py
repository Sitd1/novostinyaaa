# app/core/services/use_cases/news/classify_raw_news.py

from app.core.domain.news.entities import NewsEvent
from app.core.domain.news.repositories import NewsEventRepository
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.news.value_objects import (
    NewsEventId, Title, Summary, ImportanceLevel, Topic, Tag, Geography, EventTime
)

class ClassifyRawNewsUseCase:
    def __init__(self, news_repo: NewsEventRepository):
        self.news_repo = news_repo

    async def execute(self, raw: RawNews, ai_result: dict) -> NewsEvent:
        # ai_result – это уже результат работы агента/LLM (title, summary, tags,…)
        event = NewsEvent(
            id=NewsEventId(ai_result["id"]),
            created_at=ai_result["created_at"],
            updated_at=ai_result["created_at"],
            raw_news_ids=[raw.id],
            title=Title(ai_result["title"]),
            summary=Summary(ai_result["summary"]),
            importance=ImportanceLevel(ai_result["importance"]),
            topics=[Topic(t) for t in ai_result["topics"]],
            tags=[Tag(tag) for tag in ai_result["tags"]],
            geography=Geography(ai_result.get("geography")) if ai_result.get("geography") else None,
            event_time=EventTime(ai_result["event_time"]),
        )

        await self.news_repo.add(event)
        return event

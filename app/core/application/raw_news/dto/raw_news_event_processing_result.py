from dataclasses import dataclass, replace
from app.core.domain.news.entities import NewsEvent
from app.core.domain.raw_news.entities import RawNews


@dataclass(frozen=True)
class RawNewsEventProcessingResult:
    updated_raw_news: RawNews
    event: NewsEvent
    is_new_event: bool

    @classmethod
    def for_new_event(cls, updated_raw_news: RawNews, event: NewsEvent) -> "RawNewsEventProcessingResult":
        return cls(updated_raw_news=updated_raw_news, event=event, is_new_event=True)

    @classmethod
    def for_existing_event(cls, updated_raw_news: RawNews, event: NewsEvent) -> "RawNewsEventProcessingResult":
        return cls(updated_raw_news=updated_raw_news, event=event, is_new_event=False)

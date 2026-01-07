from dataclasses import dataclass
from entities import NewsEvent
from entities import RawNews


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

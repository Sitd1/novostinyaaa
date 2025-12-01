from dataclasses import dataclass
from app.core.domain.raw_news.entities import RawNews



@dataclass(frozen=True)
class NewsEventDraft:
    """
    Промежуточный объект для сборки NewsEvent.
    """
    title: str
    summary: str
    tags: list[str]
    importance_score: float
    raw_news_items: list[RawNews]

from dataclasses import dataclass

from app.core.domain.raw_news.entities import RawNews
from app.core.domain.news.entities import NewsEvent


@dataclass
class EventAggregationResult:
    """Результаты обработки батча сырых новостей."""
    updated_raw_news: list[RawNews]      # Новости с присвоенными event_id
    new_events: list[NewsEvent]           # Новые созданные события
    updated_events: list[NewsEvent]       # Существующие события с новыми новостями

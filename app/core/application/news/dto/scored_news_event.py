from dataclasses import dataclass
from app.core.domain.news.entities import NewsEvent



@dataclass(frozen=True)
class ScoredNewsEvent:
    event: NewsEvent
    score: float

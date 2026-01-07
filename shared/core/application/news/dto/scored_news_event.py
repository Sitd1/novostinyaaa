from dataclasses import dataclass
from entities import NewsEvent



@dataclass(frozen=True)
class ScoredNewsEvent:
    event: NewsEvent
    score: float

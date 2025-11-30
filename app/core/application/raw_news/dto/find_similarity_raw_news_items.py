from dataclasses import dataclass
from app.core.domain.raw_news.entities import RawNews


@dataclass(frozen=True)
class SimilarRawNews:
    raw_news: RawNews
    score: float


@dataclass(frozen=True)
class RawNewsCluster:
    id: str
    items: list[RawNews]

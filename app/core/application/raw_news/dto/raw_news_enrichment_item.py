from dataclasses import dataclass
from app.core.domain.raw_news.value_objects import RawNewsImportance


@dataclass(frozen=True)
class RawNewsEnrichmentResult:
    tags: list[str]
    summary: str
    importance: RawNewsImportance
    embedding: list[float]

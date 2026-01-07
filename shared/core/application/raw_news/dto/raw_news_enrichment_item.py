from dataclasses import dataclass
from value_objects import RawNewsImportance


@dataclass(frozen=True)
class RawNewsEnrichmentResult:
    tags: list[str]
    summary: str
    importance: RawNewsImportance
    embedding: list[float]

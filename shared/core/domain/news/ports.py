from typing import Protocol, Iterable

from core.domain.raw_news.entities import RawNews
from value_objects import Title, Summary, Topic, Tag, ImportanceLevel


class SimilarRawNewsFinder(Protocol):
    """Класс для поиска схожих новостей,
    объединение одной и той же новости из разных источников
    """
    def find_similar(
        self,
        base: RawNews,
        *,
        limit: int = 20,
        similarity_threshold: float = 0.8,
    ) -> list[RawNews]:
        ...


class NewsSummarizer(Protocol):
    def make_title(self, items: Iterable[RawNews]) -> Title: ...
    def make_summary(self, items: Iterable[RawNews]) -> Summary: ...
    def infer_topics(self, items: Iterable[RawNews]) -> list[Topic]: ...
    def infer_tags(self, items: Iterable[RawNews]) -> list[Tag]: ...
    def infer_importance(self, items: Iterable[RawNews]) -> ImportanceLevel: ...

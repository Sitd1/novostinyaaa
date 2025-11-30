from typing import Protocol, Iterable
from app.core.application.raw_news.dto.external_raw_news_item import ExternalRawNewsItem
from app.core.domain.raw_news.entities import RawNews


# --- ingest
class ExternalRawNewsSource(Protocol):
    """
    Порт для источника сырых новостей (Telegram, RSS, API и т.п.).
    """

    async def fetch_new_raw_items(self) -> Iterable[ExternalRawNewsItem]:
        ...


# --- processing
class TaggingService(Protocol):
    async def assign_tags(self, item: RawNews) -> list[str]:
        ...


class SummarizationService(Protocol):
    async def summarize(self, item: RawNews) -> str:
        ...


class ImportanceScoringService(Protocol):
    async def score_importance(self, item: RawNews) -> float:
        """
        Вернуть числовой скор важности (например, 0..1),
        который потом домен может маппить в ImportanceLevel.
        """
        ...


class EmbeddingService(Protocol):
    async def embed(self, item: RawNews) -> list[float]:
        ...


class RawNewsProcessingRepository(Protocol):  # ToDo - а это еще что?
    """
    Репозиторий, который умеет обновлять обогащённые поля RawNews:
    tags, summary, importance, embedding.
    """

    async def list_pending_for_processing(self, limit: int | None = None) -> list[RawNews]:
        ...

    async def save(self, item: RawNews) -> None:
        ...

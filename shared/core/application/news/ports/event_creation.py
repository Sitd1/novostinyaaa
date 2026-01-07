from typing import Protocol

from news_event_draft import NewsEventDraft
from entities import NewsEvent
from entities import RawNews


class NewsEventFactory(Protocol):
    """
    Фабрика домена: собирает NewsEvent из драфта.
    """

    def create_from_draft(self, draft: NewsEventDraft) -> NewsEvent:
        ...


class NewsEventRepository(Protocol):
    async def save(self, event: NewsEvent) -> None:
        ...


class NewsEventSummarizationService(Protocol):
    async def summarize_cluster(self, items: list[RawNews]) -> str:
        ...


class NewsEventClassificationService(Protocol):
    async def classify(
        self,
        items: list[RawNews],
    ) -> tuple[list[str], float]:
        """
        Вернуть (tags, importance_score) для итоговой новости.
        """
        ...


class TitleGenerationService(Protocol):
    async def generate_title(self, items: list[RawNews], summary: str) -> str:
        ...


class FinalTextPreparationService(Protocol):
    async def prepare_text(self, event: NewsEvent) -> str:
        """
        Подготовить финальный текст с выводом/призывом к действию.
        """
        ...
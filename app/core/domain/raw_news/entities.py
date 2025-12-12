from dataclasses import dataclass, replace
from typing import Any

from app.core.domain.raw_news.value_objects import (
    RawNewsId,
    ExternalMessageId,
    RawPublishedAt,
    RawFetchedAt,

    Tag,
    RawNewsImportance,
    RawNewsText,
    RawNewsSummary,
    RawPayload,
    RawNewsEmbedding,

    EventKey
)
from app.core.domain.sources.value_objects import SourceId, Url


@dataclass(frozen=True)
class RawNews:
    id: RawNewsId
    source_id: SourceId
    external_id: ExternalMessageId | None  # id сообщения в TG / API
    published_at: RawPublishedAt    # когда опубликовали
    fetched_at: RawFetchedAt        # когда спарсили
    text: RawNewsText               # текст сообщения
    url: Url | None                 # ссылка на саму новость
    raw_payload: RawPayload         # весь сырой json, если есть

    # заполняются после постобработки
    tags: tuple[Tag, ...] | None = None
    importance: RawNewsImportance | None = None
    summary: RawNewsSummary | None = None
    embedding: RawNewsEmbedding | None = None

    # для объединения
    event_fk: EventKey | None = None

    def __post_init__(self):
        # Простейший инвариант: не может быть "получено" раньше, чем опубликовано
        if self.fetched_at.value < self.published_at.value:
            raise ValueError(
                f"RawNews: fetched_at {self.fetched_at} < published_at {self.published_at}"
            )

    # Доменные операции постобработки (оптимизированные):

    def with_tags(self, tags: tuple[Tag, ...]) -> "RawNews":
        return replace(self, tags=tags)

    def with_summary(self, summary: RawNewsSummary) -> "RawNews":
        return replace(self, summary=summary)

    def with_importance(self, importance: RawNewsImportance) -> "RawNews":
        return replace(self, importance=importance)

    def with_embedding(self, embedding: RawNewsEmbedding) -> "RawNews":
        return replace(self, embedding=embedding)

    def with_event_key(self, event_key: EventKey) -> "RawNews":
        return replace(self, event_fk=event_key)

    # Оптимизированный метод для batch обновления (избегает цепочки .with_*())
    @classmethod
    def create_updated(
        cls,
        original: "RawNews",
        *,
        tags: tuple[Tag, ...] | None = None,
        summary: RawNewsSummary | None = None,
        importance: RawNewsImportance | None = None,
        embedding: RawNewsEmbedding | None = None,
        event_key: EventKey | None = None,
    ) -> "RawNews":
        """
        Оптимизированная версия для множественных обновлений.
        Создает только один новый объект вместо цепочки.
        """
        updates = {}
        if tags is not None:
            updates['tags'] = tags
        if summary is not None:
            updates['summary'] = summary
        if importance is not None:
            updates['importance'] = importance
        if embedding is not None:
            updates['embedding'] = embedding
        if event_key is not None:
            updates['event_fk'] = event_key

        return replace(original, **updates)


class RawNewsBuilder:
    """
    Builder для создания обновленных RawNews объектов.
    Полезен когда нужно условно обновлять поля или комбинировать обновления.

    Примеры использования:

    # Вместо цепочки .with_*()
    # news = news.with_tags(tags).with_summary(summary).with_importance(imp)

    # Используем Builder:
    builder = RawNewsBuilder(news)
    updated_news = (builder
        .with_tags(tags)
        .with_summary(summary)
        .with_importance(imp)
        .build())

    # Или условные обновления:
    updated_news = (RawNewsBuilder(news)
        .with_tags_if_present(result.tags)
        .with_summary_if_present(result.summary)
        .build())
    """

    def __init__(self, original: RawNews):
        self._original = original
        self._updates: dict[str, Any] = {}

    def with_tags(self, tags: tuple[Tag, ...]) -> "RawNewsBuilder":
        self._updates['tags'] = tags
        return self

    def with_summary(self, summary: RawNewsSummary) -> "RawNewsBuilder":
        self._updates['summary'] = summary
        return self

    def with_importance(self, importance: RawNewsImportance) -> "RawNewsBuilder":
        self._updates['importance'] = importance
        return self

    def with_embedding(self, embedding: RawNewsEmbedding) -> "RawNewsBuilder":
        self._updates['embedding'] = embedding
        return self

    def with_event_key(self, event_key: EventKey) -> "RawNewsBuilder":
        self._updates['event_fk'] = event_key
        return self

    def build(self) -> RawNews:
        """Создает новый объект с накопленными обновлениями."""
        return replace(self._original, **self._updates)

    def clear(self) -> "RawNewsBuilder":
        """Очищает накопленные обновления."""
        self._updates.clear()
        return self

    # Удобные методы для условных обновлений
    def with_tags_if_present(self, tags: tuple[Tag, ...] | None) -> "RawNewsBuilder":
        """Обновляет tags только если они не None."""
        if tags is not None:
            self._updates['tags'] = tags
        return self

    def with_summary_if_present(self, summary: RawNewsSummary | None) -> "RawNewsBuilder":
        """Обновляет summary только если он не None."""
        if summary is not None:
            self._updates['summary'] = summary
        return self

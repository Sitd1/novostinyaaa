from __future__ import annotations

from typing import Protocol, Iterable
from abc import abstractmethod

from entities import RawNews
from value_objects import (
    RawNewsId,
    ExternalMessageId,
    Source,
)


class RawNewsRepository(Protocol):
    """
    Доменный порт для работы с сырыми новостями.

    Никаких деталей БД / ORM. Только то, что нужно use-cases.
    """

    # --- базовые CRUD-операции ---

    @abstractmethod
    def add(self, item: RawNews) -> RawNews:
        """
        Сохранить одну сырую новость.
        Возврат того же объекта или копии с проставленным id — на совести реализации.
        """

    @abstractmethod
    def add_many(self, items: Iterable[RawNews]) -> None:
        """
        Сохранить пачку сырых новостей.
        Конкретная реализация может делать bulk insert.
        """

    @abstractmethod
    def get_by_id(self, raw_news_id: RawNewsId) -> RawNews | None:
        """Найти новость по внутреннему id."""

    @abstractmethod
    def get_by_external_id(
        self,
        source: Source,
        external_id: ExternalMessageId,
    ) -> RawNews | None:
        """
        Найти новость по связке `source + external_id`.
        Нужен и для дедупликации, и для возможного обновления.
        """

    # --- операции, связанные с постобработкой ---

    @abstractmethod
    def list_for_postprocessing(
        self,
        *,
        limit: int = 100,
    ) -> list[RawNews]:
        """
        Вернуть пачку сырых новостей, которые ещё не прошли постобработку.

        Типичный критерий (реализация решает сама):
        - tags is None ИЛИ
        - interest_importance is None ИЛИ
        - summary is None
        """

    @abstractmethod
    def update_news(self, item: RawNews) -> None:
        """
        Обновить новость (например, после того как сервис дополнил
        tags / interest_importance / summary).

        Поскольку RawNews — frozen dataclass, ожидается, что
        доменный сервис создаёт обновлённую копию (через dataclasses.replace)
        и передаёт её сюда.
        """

    @abstractmethod
    def update_news_many(self, items: Iterable[RawNews]) -> None:
        """
        Массовое обновление — для батчевой постобработки новостей.
        """

    # --- вспомогательное (для дедупликации и быстрых проверок) ---

    @abstractmethod
    def exists_by_external_id(
        self,
        source: Source,
        external_id: ExternalMessageId,
    ) -> bool:
        """
        Быстрая проверка на существование (для дедупликации).
        Можно использовать перед add/add_many.
        """


from typing import Protocol
from external_raw_news_item import ExternalRawNewsItem
from entities import RawNews


class RawNewsFactory(Protocol):
    def create_from_external(self, item: ExternalRawNewsItem) -> RawNews:
        ...
# доменные порты – их будут реализовывать адаптеры в инфраструктуре
# (SQLAlchemy-репозиторий, конкретная фабрика и т.п.
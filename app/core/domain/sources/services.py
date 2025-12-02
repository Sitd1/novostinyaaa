from typing import Protocol
from app.core.application.raw_news.dto.external_raw_news_item import ExternalRawNewsItem
from app.core.domain.raw_news.entities import RawNews


class RawNewsFactory(Protocol):
    def create_from_external(self, item: ExternalRawNewsItem) -> RawNews:
        ...
# доменные порты – их будут реализовывать адаптеры в инфраструктуре
# (SQLAlchemy-репозиторий, конкретная фабрика и т.п.
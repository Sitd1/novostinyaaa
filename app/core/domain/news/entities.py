# Тут живут сущности, например:
#
# * `News` – новость:
#
#   * id, заголовок, текст, источник, время, важность и т.п.
# * `RawNews` – сырая новость из телеграм/гугл/ещё откуда-то.
# * `RunStory` или аналог – сущность про «запуск обработки новостей» (например, одна итерация скрейпа).
import datetime
# Сущности:
#
# * имеют идентичность (id),
# * содержат бизнес-логику (например, метод `mark_as_important()`).
from dataclasses import dataclass


@dataclass
class RawNews:
    id: RawNewsId
    source_id: NewsSourceId
    title: Title
    content: Content
    published_at: datetime


@dataclass
class News:
    """Отвечает за целостность одной новостной единицы."""
    id: NewsId
    source_id: NewsSourceId
    title: Title  # (VO)
    content: Content  # (VO)
    published_at: datetime
    tags: List[Tag]
    importance_score: ImportanceScore  # (VO, результат работы агента)
    status: NewsStatus  # (VO: raw, filtered, published)
    ...

@dataclass
class NewsSource:
    """Описание источника новости (tg, RSS, сайт)"""
    id: NewsSourceId
    name: NewsSourceName
    url: URL
    is_active: bool
    ...

@dataclass
class Tag:
    id: Tagid
    name: str
    description: str | None







# Тут **интерфейсы репозиториев**, а не реализация:
#
# * `class NewsRepository(Protocol): ...`
# * `class RawNewsRepository(Protocol): ...`
# * `class RunsStoryRepository(Protocol): ...`
#
# Определяют:
#
# * какие методы нужны домену/юзкейсам:
#
#   * `get_latest()`, `save(news)`, `list_unprocessed()`, `mark_processed(...)` и т.п.
# * **без** SQLAlchemy, без моделей БД, без подключения.
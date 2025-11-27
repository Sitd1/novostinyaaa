from datetime import datetime, timezone, date
from typing import Any

from agents.utils.state import OneNews, SearchResult
from database.models.runs_story import RunsStory
from database.async_connection.session import get_session
from database.repositories.runs_story import RunsStoryRepository
from database.repositories.news import NewsRepository


def one_news_to_dict(news: OneNews) -> dict[str, Any]:
    return {
        "title": news.title,
        "summary": news.summary,
        "source_name": news.source_name,
        "source_url": news.source_url,
        # если в БД колонка Date/DateTime — лучше сразу превратить:
        "published_at": date.fromisoformat(news.published_at),
        "relevance_reasoning": news.relevance_reasoning,
    }


async def create_search_run_with_news(news_items: list[dict]) -> RunsStory:
    async with get_session() as session:
        runs_repo = RunsStoryRepository(session)
        news_repo = NewsRepository(session)

        # 1. создаём run
        run = RunsStory(
            datetime=datetime.now(timezone.utc),
            news_count=len(news_items),
        )
        await runs_repo.add(run)  # тут после flush у него появится id

        # 2. создаём новости и привязываем к run по run.id
        await news_repo.save_many_for_run(run.id, news_items)

        # commit сделает get_session
        return run

async def create_search_run_with_news_from_search_result(search_result: SearchResult) -> RunsStory:
    news_items = [one_news_to_dict(n) for n in search_result.news_list]
    return await create_search_run_with_news(news_items)
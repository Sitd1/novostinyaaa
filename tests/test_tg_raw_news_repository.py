import asyncio

from app.infrastructure.database.session import get_async_session
from app.infrastructure.database.repositories.tg_raw_news import TgRawNewsRepository
from app.core.domain.raw_news.value_objects import RawNewsId


async def test_tg_raw_news_repository():
    async with get_async_session() as session:
        repo = TgRawNewsRepository(session=session)
        # id = await repo.get_last_message_id(channel_username='lentach')
        raw_news_id = RawNewsId(1)
        id = await repo.get(id=raw_news_id)

        print('-' * 100)
        print(id)
        print('-' * 100)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_tg_raw_news_repository())
    loop.close()



from sqlalchemy.ext.asyncio import AsyncSession
from database.repositories.base import BaseRepository
from database.models.runs_story import RunsStory


class RunsStoryRepository(BaseRepository[RunsStory]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RunsStory)

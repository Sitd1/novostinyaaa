from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from shared.database.async_connection.engine import engine as async_engine

# Фабрика сессий
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Объекты остаются доступными после коммита
    autocommit=False,
    autoflush=False,
)


# Контекстный менеджер для работы с сессией
@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный контекстный менеджер для получения сессии БД.

    Использование:
        async with get_session() as session:
            result = await session.execute(query)
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# # Dependency для FastAPI (если используете)
# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     """
#     Dependency для FastAPI эндпоинтов.
#
#     Использование:
#         @app.get("/items")
#         async def get_items(session: AsyncSession = Depends(get_db_session)):
#             ...
#     """
#     async with get_session() as session:
#         yield session

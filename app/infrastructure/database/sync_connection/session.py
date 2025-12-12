from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager
from typing import Generator

from app.infrastructure.database.sync_connection.engine import engine as sync_engine

# Фабрика сессий
async_session_maker = sessionmaker(
    sync_engine,
    class_=Session,
    expire_on_commit=False,  # Объекты остаются доступными после коммита
    autocommit=False,
    autoflush=False,
)


# Контекстный менеджер для работы с сессией
@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Синхронный контекстный менеджер для получения сессии БД.

    Использование:
        with get_session() as session:
            result = session.execute(query)
    """
    with async_session_maker() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

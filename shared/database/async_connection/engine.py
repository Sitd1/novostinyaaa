from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from config import Config

config = Config()



# URL подключения к БД
DATABASE_URL = config.db.url_asyncpg

# Создание асинхронного движка
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логирование SQL запросов (отключите в продакшене)
    pool_size=5,  # Размер пула соединений
    max_overflow=10,  # Максимальное количество дополнительных соединений
    pool_pre_ping=True,  # Проверка соединения перед использованием
)

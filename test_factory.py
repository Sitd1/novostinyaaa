#!/usr/bin/env python3
"""
Простой тест для проверки работоспособности функции create_telegram_raw_news_source.
"""
import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.infrastructure.crawler.tg_crawler.factory import create_telegram_raw_news_source
from app.infrastructure.crawler.tg_crawler.raw_news_source import TelegramRawNewsSource
from app.infrastructure.database.repositories.tg_raw_news import TgRawNewsRepository


async def test_create_telegram_raw_news_source():
    """Тест создания TelegramRawNewsSource через фабрику."""
    print("Тестируем функцию create_telegram_raw_news_source...")

    # Создаем mock сессию
    mock_session = AsyncMock()

    # Создаем mock Telegram клиента
    mock_client = MagicMock()

    try:
        # Мокаем get_telegram_client функцию
        with patch('app.infrastructure.crawler.tg_crawler.factory.get_telegram_client', return_value=mock_client):
            # Вызываем функцию фабрики
            result = await create_telegram_raw_news_source(mock_session)

            # Проверяем тип результата
            assert isinstance(result, TelegramRawNewsSource), f"Ожидался TelegramRawNewsSource, получен {type(result)}"

            # Проверяем, что объект правильно инициализирован
            assert hasattr(result, 'client'), "Объект должен иметь атрибут client"
            assert hasattr(result, 'repo'), "Объект должен иметь атрибут repo"
            assert hasattr(result, 'channels'), "Объект должен иметь атрибут channels"
            assert hasattr(result, 'limit_per_channel'), "Объект должен иметь атрибут limit_per_channel"

            # Проверяем типы атрибутов
            assert isinstance(result.repo, TgRawNewsRepository), f"repo должен быть TgRawNewsRepository, получен {type(result.repo)}"

            # Проверяем значения
            assert result.limit_per_channel == 50, f"limit_per_channel должен быть 50, получен {result.limit_per_channel}"
            assert result.client == mock_client, "client должен быть нашим mock объектом"

            print("✅ Функция create_telegram_raw_news_source работает корректно!")
            print(f"   Тип результата: {type(result)}")
            print(f"   limit_per_channel: {result.limit_per_channel}")
            print(f"   Количество каналов: {len(result.channels)}")

            return True

    except Exception as e:
        print(f"❌ Ошибка при выполнении функции: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_imports():
    """Тест, что все импорты работают."""
    print("Тестируем импорты...")

    try:
        # Проверяем импорты
        from app.infrastructure.crawler.tg_crawler.factory import create_telegram_raw_news_source
        from app.infrastructure.crawler.tg_crawler.raw_news_source import TelegramRawNewsSource
        from app.infrastructure.database.repositories.tg_raw_news import TgRawNewsRepository
        from app.infrastructure.crawler.tg_crawler.client import get_telegram_client

        print("✅ Все импорты успешны!")
        return True

    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False


async def main():
    """Главная функция теста."""
    print("🚀 Начинаем тестирование функции create_telegram_raw_news_source")
    print()

    # Тест импортов
    imports_ok = await test_imports()
    if not imports_ok:
        return False

    print()

    # Тест функции
    function_ok = await test_create_telegram_raw_news_source()
    if not function_ok:
        return False

    print()
    print("🎉 Все тесты пройдены успешно!")
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
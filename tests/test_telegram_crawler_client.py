import asyncio
from app.infrastructure.crawler.tg_crawler.client import get_telegram_client


async def test_telegram_client():
    """Проверка подключения к Telegram"""
    client = get_telegram_client()

    try:
        # Подключаемся к Telegram
        await client.start()
        print("✓ Успешно подключились к Telegram")

        # Получаем информацию о текущем пользователе
        me = await client.get_me()
        print(f"✓ Авторизован как: {me.first_name} (@{me.username})")
        print(f"  ID: {me.id}")
        print(f"  Телефон: {me.phone}")

        # Проверяем, что можем получать диалоги
        dialogs = await client.get_dialogs(limit=5)
        print(f"✓ Найдено диалогов: {len(dialogs)}")
        for dialog in dialogs[:3]:
            print(f"  - {dialog.name}")

        print("\n✓ Все проверки пройдены успешно!")

    except Exception as e:
        print(f"✗ Ошибка: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    telegram_client = get_telegram_client()

    # Запускаем проверку
    asyncio.run(test_telegram_client())
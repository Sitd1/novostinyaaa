# airflow_data/dags/crawler_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import logging

# Импортируем существующую функцию crawler
from apps.crawler.services.tg_crawler.probe_collect import collect_last_messages

# Настройка логгера
logger = logging.getLogger(__name__)


# Обертка для безопасного выполнения с обработкой ошибок
def safe_collect_messages(**context):
    """
    Безопасная обертка для сбора сообщений из Telegram
    """
    try:
        logger.info("Начинаем сбор сообщений из Telegram каналов")

        limit_per_channel = context.get('limit_per_channel', 50)

        # Вызов основной функции
        result = collect_last_messages(limit_per_channel=limit_per_channel)

        logger.info(f"Сбор сообщений завершен успешно: {result}")
        return result

    except Exception as e:
        logger.error(f"Ошибка при сборе сообщений: {str(e)}", exc_info=True)
        raise


# Аргументы по умолчанию для DAG
default_args = {
    'owner': 'news_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 1),  # Используем обычный datetime
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(minutes=10),
}

# Создание DAG с использованием context manager
with DAG(
        dag_id='telegram_crawler',
        default_args=default_args,
        description='Сбор новостей из Telegram каналов каждые 15 минут',
        schedule_interval='*/15 * * * *',  # Каждые 15 минут
        catchup=False,
        max_active_runs=1,
        tags=['telegram', 'crawler', 'news', 'production'],
) as dag:
    # Задача для сбора новостей
    crawl_task = PythonOperator(
        task_id='collect_telegram_news',
        python_callable=safe_collect_messages,
        op_kwargs={'limit_per_channel': 50},
    )
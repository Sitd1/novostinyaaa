include .env
export

.PHONY: setup up down logs clean migrate-create migrate-up

# Полный запуск проекта с нуля
setup:
	@echo "Остановка и удаление старых томов..."
	docker compose down -v
	@echo "Настройка прав для скрипта БД..."
	chmod +x init-multiple-dbs.sh
	@echo "Запуск сборки и контейнеров..."
	docker compose up -d --build
	@echo "Ожидание готовности БД..."
	sleep 5
	@echo "Применение миграций..."
	$(MAKE) migrate-up
	@echo "Проект запущен. Базы созданы, таблицы на месте."

# Создание новой миграции (использование: make migrate-create msg="add_users_table")
migrate-create:
	docker compose exec api alembic revision --autogenerate -m "$(msg)"

# Применение существующих миграций
migrate-up:
	docker compose exec api alembic upgrade head

# Откат последней миграции
migrate-down:
	docker compose exec api alembic downgrade -1

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f api

reset-db:
	docker compose stop airflow-webserver airflow-scheduler airflow-init api db
	docker compose rm -f airflow-webserver airflow-scheduler airflow-init api db
	docker volume rm $$(docker volume ls -q | grep postgres_data) || true
	make setup
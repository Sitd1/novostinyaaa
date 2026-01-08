include .env
export

.PHONY: setup up down logs clean

# Самая важная команда: чистит всё и запускает с нуля
setup:
	@echo "Остановка и удаление старых томов..."
	docker compose down -v
	@echo "Настройка прав для скрипта БД..."
	chmod +x init-multiple-dbs.sh
	@echo "Запуск сборки и контейнеров..."
	docker compose up -d --build
	@echo "Проект запущен. БД инициализированы."

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

# Если нужно только сбросить базу и Airflow, не пересобирая образы
reset-db:
	docker compose stop airflow-webserver airflow-scheduler airflow-init api db
	docker compose rm -f airflow-webserver airflow-scheduler airflow-init api db
	docker volume rm $$(docker volume ls -q | grep postgres_data) || true
	make up
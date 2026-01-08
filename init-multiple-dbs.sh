#!/bin/bash
set -e

# Проверяем, что переменная не пустая, прежде чем стрелять в базу
if [ -z "$AIRFLOW_DB_NAME" ]; then
    echo "Ошибка: AIRFLOW_DB_NAME не задана!"
    exit 1
fi

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE "$AIRFLOW_DB_NAME";
EOSQL
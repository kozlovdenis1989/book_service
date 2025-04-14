#!/bin/sh
# app/start.sh

# Небольшая пауза перед миграциями
sleep 5

# Выполняем миграции
alembic upgrade head || { echo "Migration failed"; exit 1; }

# Запускаем приложение
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

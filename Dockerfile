# Dockerfile


FROM python:3.12-slim


WORKDIR /app

# Копируем файлы requirements и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию
COPY ./app /app/app

# Копируем папку alembic в рабочую директорию
COPY ./alembic ./alembic
COPY alembic.ini ./
COPY start.sh ./

# Команда для запуска приложения
CMD ["./start.sh"]

# Команда для запуска приложения
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
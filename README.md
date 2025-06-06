# Book REST API

      Приложение на FastAPI для управления бронированиями. Можно выполнять CRUD операции со столиками и бронировать их на определенные дату, время и продолжительность. Сервис гарантирует, что время бронирований на одном столике не будут пересекаться.

│  
├── app/                     # Папка с приложением  
│   ├── __init__.py  
│   ├── db.py                # Работа с бд  
│   ├── main.py              # Основной файл с FastAPI приложением  
│   ├── models.py              # Модели данных  
│   ├── schemas.py             # Схемы для валидации данных  
│   ├── services/            # Логика работы с данными  
│   └── routers/             # Роутеры для обработки запросов  
│  
├── alembic/                   
│   ├── versions/            # Папка с  миграциями  
│   └── env.py               # Конфигурации Alembic  
│  
├── alembic.ini              # Файл конфигурации Alembic   
│── Dockerfile               #  Docker файл  
│── docker-compose.yml       #  Docker compose  
│── .env                     #  Файл с переменными окружения  
│  
├── tests/                   # Тесты  
│   │  
│   ├── test_desks.py  
│   └── test_reservation.py  
└── requirements.txt         # Список зависимостей  

## Запуск из виртуальной среды

Убедитесь, что у вас установлен Python 3.12 и pip. Установите необходимые зависимости с помощью:

```bash
pip install -r requirements.txt
```

Измените настройки подключения к своей локальной базе Postgres в файлах db.py и alembic.ini.



## Запуск проекта в Docker

## Перед запуском:

Убедитесь, что у вас установлены Docker и Docker Compose. Вы можете установить их, следуя инструкциям на официальных страницах.
Измените настроки Postgress в alembic.ini и .env 

### Стандартные команды

1. **Сборка и запуск контейнеров**:

   Чтобы собрать и запустить все сервисы, выполните:

   ```bash
   docker-compose up --build
   ```

2. **Остановка контейнеров**:

   Чтобы остановить контейнеры:

   ```bash
   docker-compose stop
   ```

   Чтобы остановить и удалить контейнеры, выполните:

   ```bash
   docker-compose down --volumes
   ```

### Обращение к API

После успешного запуска сервер доступен по адресу:

```
http://localhost:8000/docs
```

Это документация Swagger, где вы можете тестировать API.

### Примечания

- При первом запуске Alembic выполнит миграции и создаст необходимые таблицы в базе данных.
- Если вы изменили настройки подключения к базе данных в `docker-compose.yml` или `alembic.ini`, убедитесь, что они совпадают.

## Запуск тестов в docker

запустите docker-compose с флагом -d

```bash
docker-compose up -d
```
выведите список процессов 

```bash
docker ps
```
найдите имя запущеного процесса приложения (образ change-web) и выполниет команду для запуска оболочки

```bash
docker exec -it <имя процесса> /bin/bash
```

Для проверки функциональности приложения выполните:

```bash
pytest tests/test_desks.py
pytest tests/test_reservation.py
```

## Стек технологий

- **FastAPI**: 
- **SQLAlchemy**: 
- **PostgreSQL**:
- **Docker**: 

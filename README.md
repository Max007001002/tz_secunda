# Справочник организаций (REST API)

## Запуск локально

1. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Создать файл `.env` с нужными переменными (см. ниже).
3. Запустить приложение:
   ```bash
   uvicorn app.main:app --reload
   ```

После запуска документация будет доступна по адресу `http://127.0.0.1:8000/docs`.

## Переменные окружения

Для работы приложения нужны переменные в `.env`:

- `DATABASE_URL`
- `DATABASE_SYNC_URL`
- `API_KEY`
- `DEBUG` (опционально)

## Запуск через Docker

1. Создать файл `.env` рядом с `docker-compose.yml`:
   ```env
   DATABASE_URL=postgresql+asyncpg://org_user:org_password@db:5432/org_directory_db
   DATABASE_SYNC_URL=postgresql+psycopg2://org_user:org_password@db:5432/org_directory_db
   API_KEY=CHANGE_ME
   DEBUG=false
   ```
2. Поднять сервисы:
   ```bash
   docker compose up -d --build
   ```
3. Применить миграции (включая тестовые данные):
   ```bash
   docker compose exec api alembic upgrade head
   ```
4. Открыть документацию: `http://localhost:8000/docs`

Все запросы требуют заголовок `X-API-Key` со значением из `.env`.

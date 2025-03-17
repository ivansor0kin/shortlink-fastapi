# Веб-сервис для сокращения ссылок

FastAPI-приложение для создания, управления и отслеживания коротких ссылок с кэшированием через Redis.

## API

- **POST /links/shorten**: Создает короткую ссылку.
  - Параметры: `original_url` (обязательный), `custom_alias` (опциональный), `expires_at` (опциональный).
- **GET /links/{short_code}**: Возвращает информацию о ссылке.
- **DELETE /links/{short_code}**: Удаляет ссылку.
- **PUT /links/{short_code}**: Обновляет URL.
- **GET /links/{short_code}/stats**: Статистика по ссылке.
- **GET /links/search?original_url={url}**: Поиск по оригинальному URL.
- **GET /links/expired**: Список истекших ссылок.

## Примеры запросов

1. Создание ссылки:
```bash
curl -X POST "http://localhost:8000/links/shorten" -d '{"original_url": "https://example.com"}' -H "Content-Type: application/json"
```
2. Получение информации:
```bash
curl "http://localhost:8000/links/abc123"
```

## Локальный запуск

1. Установите Docker и Docker Compose.
2. Выполните:
```bash
docker-compose up --build
```
3. API будет доступно на http://localhost:8000.
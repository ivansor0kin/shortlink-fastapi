# Веб-сервис для сокращения ссылок

FastAPI-приложение для создания, управления и отслеживания коротких ссылок с регистрацией пользователей, кэшированием через Redis и хранением данных в PostgreSQL. Развертывание осуществляется исключительно на Render.com.

## API

### Аутентификация
- **POST /register**: Регистрация нового пользователя.
  - Тело запроса: `{"username": "string", "password": "string"}`
  - Ответ: `{"access_token": "string", "token_type": "bearer"}`

- **POST /token**: Получение токена для авторизации.
  - Тело запроса: `{"username": "string", "password": "string"}`
  - Ответ: `{"access_token": "string", "token_type": "bearer"}`

### Ссылки
- **POST /links/shorten**: Создает короткую ссылку (требуется авторизация).
  - Тело запроса: `{"original_url": "string", "custom_alias": "string", "expires_at": "datetime"}`
  - Ответ: `{"id": int, "original_url": "string", "short_code": "string", "created_at": "datetime", "expires_at": "datetime", "user_id": int}`

- **GET /links/{short_code}**: Перенаправляет на оригинальный URL.
  - Ответ: `{"original_url": "string"}`

- **DELETE /links/{short_code}**: Удаляет ссылку (требуется авторизация).
  - Ответ: `{"message": "Link deleted"}`

- **PUT /links/{short_code}**: Обновляет ссылку (требуется авторизация).
  - Тело запроса: `{"original_url": "string"}`
  - Ответ: `{"id": int, "original_url": "string", "short_code": "string", "created_at": "datetime", "expires_at": "datetime", "user_id": int}`

- **GET /links/{short_code}/stats**: Получает статистику по ссылке.
  - Ответ: `{"original_url": "string", "created_at": "string", "clicks": int, "last_used": "string"}`

- **GET /links/search?original_url={url}**: Ищет короткую ссылку по оригинальному URL.
  - Ответ: `{"short_code": "string"}`

## Примеры запросов
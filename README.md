# Shortlink FastAPI

## Описание

Это REST API для создания, управления и поиска коротких ссылок. Поддерживает авторизацию пользователей, создание ссылок с кастомными или случайными короткими кодами, а также базовую статистику использования. API построен на FastAPI, использует PostgreSQL для хранения данных и Redis для кэширования. Все три элемента были развернуты на Render.com.

### Доступ

API уже развернуто на Render.com и доступно вместе с Swagger-документацией по ссылке https://shortlink-fastapi.onrender.com/docs. Бесплатный хостинг прекратится 04/04/2025.

## Основные возможности:
- Регистрация и авторизация пользователей через JWT-токены.
- Создание коротких ссылок с указанием срока действия.
- Поиск ссылок по оригинальному URL.
- Получение статистики по использованию ссылок.

## Примеры запросов

### 1. Получение токена (авторизация)
```bash
curl -X 'POST' \
  'https://shortlink-fastapi.onrender.com/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=test&password=test123'
```
### Ответ
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
### 2. Создание короткой ссылки
```bash
curl -X 'POST' \
  'https://shortlink-fastapi.onrender.com/links/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <your-token>' \
  -H 'Content-Type: application/json' \
  -d '{"original_url": "https://example.com", "short_code": "exmpl"}'
```
### Ответ
```json
{
  "id": 1,
  "original_url": "https://example.com",
  "short_code": "exmpl",
  "created_at": "2025-03-17T12:00:00",
  "expires_at": "2025-04-16T12:00:00",
  "last_used": null,
  "clicks": 0,
  "user_id": 1
}
```
### 3. Поиск ссылки по оригинальному URL
```bash
curl -X 'GET' \
  'https://shortlink-fastapi.onrender.com/links/search?original_url=https%3A%2F%2Fexample.com' \
  -H 'accept: application/json'
```
### Ответ
```json
[
  {
    "id": 1,
    "original_url": "https://example.com",
    "short_code": "exmpl",
    "created_at": "2025-03-17T12:00:00",
    "expires_at": "2025-04-16T12:00:00",
    "last_used": null,
    "clicks": 0,
    "user_id": 1
  }
]
```
### 4. Получение статистики по короткой ссылке
```bash
curl -X 'GET' \
  'https://shortlink-fastapi.onrender.com/links/stats/exmpl' \
  -H 'accept: application/json'
```
### Ответ
```json
{
  "original_url": "https://example.com",
  "short_code": "exmpl",
  "clicks": 0,
  "created_at": "2025-03-17T12:00:00",
  "expires_at": "2025-04-16T12:00:00",
  "last_used": null
}
```
## Инструкция по запуску (для тестирования)

### Чтобы протестировать его, выполните следующие шаги:

1. Откройте документацию Swagger:
- Перейдите в браузере по вышеуказанной ссылке. 
- Здесь вы увидите все доступные эндпоинты и сможете их протестировать.
2. Получите токен:
- В Swagger найдите POST /register.
- Нажмите "Try it out".
- Придумайте и введите username и password.
- После регистрации нажмите "Authorize", чтобы войти (логин).
3. Протестируйте эндпоинты:
- В Swagger выберите любой эндпоинт (например, POST /links/).
- Заполните необходимые поля и выполните запрос, нажав "Execute".
4. Используйте curl (альтернатива):
- В Swagger найдите POST /token.
- Нажмите "Try it out".
- Введите username и password (если пользователь уже создан через /register).
- Скопируйте примеры запросов выше, заменив <your-token> на ваш токен.
- Выполните их в терминале.
- Примечание: Если у вас нет пользователя, вам нужно создать его напрямую через /register.

## Описание базы данных

### API использует PostgreSQL для хранения данных. Схема включает две основные таблицы:

1. Таблица users
- id: Integer, первичный ключ, автоинкремент.
- username: String, уникальный логин пользователя.
- hashed_password: String, хэшированный пароль (с использованием passlib).
- links: Связь один-ко-многим с таблицей links.
2. Таблица links
- id: Integer, первичный ключ, автоинкремент.
- original_url: String, исходный URL (индексируется).
- short_code: String, короткий код ссылки (уникальный, индексируется).
- created_at: DateTime, дата создания (по умолчанию — текущая).
- expires_at: DateTime, срок действия (опционально).
- last_used: DateTime, дата последнего использования (опционально).
- clicks: Integer, количество переходов (по умолчанию 0).
- user_id: Integer, внешний ключ на users.id (опционально, nullable).
- user: Связь многие-к-одному с таблицей users.

## Тестирование и покрытие кода

В репозитории присутствуют тесты (папка `tests`), проверяющие корректность основных сценариев использования. 

Чтобы запустить тесты с покрытием, выполните:

```bash
coverage run -m pytest tests
coverage html
```

После этого будет создана папка `htmlcov` с файлом `index.html`, где можно увидеть подробный отчёт о покрытии.

### Краткая сводка покрытия `tests/htmlcov/index.html` (возможно скачать и открыть в браузере)

| Module                   | Statements | Missing | Coverage |
|--------------------------|-----------:|--------:|---------:|
| **app/__init__.py**      | 0         | 0       | 100%     |
| **app/auth.py**          | 41        | 4       | 90%      |
| **app/cache.py**         | 10        | 0       | 100%     |
| **app/config.py**        | 5         | 0       | 100%     |
| **app/database.py**      | 12        | 0       | 100%     |
| **app/main.py**          | 7         | 0       | 100%     |
| **app/models.py**        | 21        | 0       | 100%     |
| **app/routers/__init__.py** | 0      | 0       | 100%     |
| **app/routers/links.py** | 61        | 21      | 66%      |
| **app/routers/users.py** | 27        | 0       | 100%     |
| **app/schemas.py**       | 29        | 0       | 100%     |
| **app/services.py**      | 64        | 0       | 100%     |
| **app/utils.py**         | 5         | 0       | 100%     |
| **Total**                | 282       | 25      | **91%**  |

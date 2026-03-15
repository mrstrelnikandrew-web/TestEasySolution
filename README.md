# Deribit Crypto Tracker

Сервис для мониторинга котировок BTC и ETH. Система собирает данные с биржи Deribit и предоставляет REST API для доступа к истории цен.

## Design Decisions

1. Async FastAPI & SQLAlchemy: Выбрал асинхронный стек, чтобы API не блокировалось при ожидании ответов от БД или биржи. Это критично для высокой нагрузки.
2. Celery + asyncio.run: Так как Celery синхронен, использовал обертку asyncio.run. Это позволило не переписывать логику воркера и сохранить единый асинхронный стиль в aiohttp и asyncpg.
3. Pydantic V2: Отвечает за строгую валидацию и автоматические схемы ответов.
4. Архитектура: Разделил проект на слои (api, services, tasks, db). Код проще поддерживать, когда логика работы с биржей не перемешана с эндпоинтами.
5. Индексация: Добавил индексы на поля ticker и timestamp. Без них выборка по истории цен начала бы тормозить уже через пару дней работы.

## Развертывание

Проект полностью контейнеризирован.

```bash
docker-compose up --build
```

## Доступные сервисы:
* API: http://localhost:8000
* Swagger UI: http://localhost:8000/docs
* Redis: localhost:6379
* PostgreSQL: localhost:5432

### Структура проекта
```
├── app
│   ├── api           # Обработчики запросов
│   ├── core          # Конфигурация (Pydantic Settings)
│   ├── db            # SQLAlchemy модели и сессии
│   ├── schemas       # Pydantic DTO (валидация данных)
│   ├── services      # Логика работы с внешним API
│   └── tasks         # Фоновые задачи (Celery)
├── tests             # Pytest сценарии
├── docker-compose.yml
└── requirements.txt
```

### Методы API

Метод|Описание|Параметры
|----------|----------|----------|
|/prices/all|Вся история цен|ticker|
|/prices/last|Актуальная цена|ticker|
|/prices/filter|Фильтр по дате|ticker, start_ts, end_ts|

## Тестирование

В проект включены Unit-тесты для проверки работы API и корректности обработки тикеров.Bashdocker-compose exec api pytest

#API CONTRACT

## 1. GET /tasks - получить список задач

**Query Parameters:**

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| status | string | false | Фильтр по статусу | `?status=completed` |

**Status Codes:**
- `200 OK` - успешный ответ
- `400 Bad Request` - неверные параметры запроса
- `422 Unprocessable Entity` - неверные типы данных

**Success Response Body (200 OK):**

```json
{  
  "id": "int",
  "title": "string",
  "description": "string",
  "status": "pending|in_progress|completed",
  "user_id": "int | null",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

**Error response:**
```json
{
  "error": "BAD_REQUEST",
  "message": "Параметр 'status' должен быть одним из: pending, in_progress, completed",
  "timestamp": "2025-04-15T10:30:00Z"
}
```

## 2. GET /tasks/{task_id} - получить задачу

**Status Codes:**
- `200 OK` - успешный ответ
- `404 Not Found` - задача не найдена
- `422 Unprocessable Entity` - неверные типы данных

**Success Response Body (200 OK):**
```json
{
  "id": 1,
  "title": "Купить молоко",
  "description": "Купить 2 литра молока в магазине",
  "status": "pending",
  "user_id": null,
  "created_at": "2025-04-15T09:00:00Z",
  "updated_at": "2025-04-15T09:00:00Z"
}
```

**Error response:**
```json
{
  "error": "NOT_FOUND",
  "message": "Задание не найдено",
  "timestamp": "2025-04-15T10:30:00Z"
}
```

## 3. POST /tasks — создать новую задачу

### Request Body

| Поле | Тип | Обязательный | Описание |
|------|-----|--------------|----------|
| title | строка | **да** | Название задачи |
| description | строка | нет | Описание задачи |

**Status Codes:**
- `201 OK` - задача создана
- `400 Bad Request` - неверные параметры запроса
- `422 Unprocessable Entity` - неверные типы данных

**Success Response Body (201 OK):**
```json
{
  "id": 1,
  "title": "Написать отчет",
  "description": "Подготовить квартальный отчет для клиента",
  "status": "pending",
  "user_id": null,
  "created_at": "2025-04-15T10:30:00Z",
  "updated_at": "2025-04-15T10:30:00Z"
}
```

**Error response:**
```json
{
  "error": "BAD_REQUEST",
  "message": "Параметр 'priority' должен быть одним из: low, medium, high",
  "timestamp": "2025-04-15T10:30:00Z"
}
```

## 4. PATCH /tasks/{task_id} - частично обновить задачу

### Разрешённые поля для PATCH

| Поле | Тип | Что делает `null` |
|------|-----|-------------------|
| title | string | Запрещено (нельзя сделать null) |
| description | string | ✅ Очищает описание |
| status | string | Запрещено (нельзя сделать null) |

### Request Body 
```json
{
  "id": "int",
  "title": "string",
  "description": "string",
  "status": "pending|in_progress|completed",
  "user_id": "int | null",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
  }
```

**Status Codes:**
- `200 OK` - задача изменена
- `400 Bad Request` - неверные параметры запроса
- `422 Unprocessable Entity` - неверные типы данных

**Success Response Body (201 OK):**
```json
{
  "id": 1,
  "title": "Написать отчет",
  "description": "Подготовить квартальный отчет для клиента",
  "status": "pending",
  "user_id": null,
  "created_at": "2025-04-15T10:30:00Z",
  "updated_at": "2025-04-15T10:30:00Z"
}
```

**Error response:**
```json
{
  "error": "BAD_REQUEST",
  "message": "Параметр 'priority' должен быть одним из: low, medium, high",
  "timestamp": "2025-04-15T10:30:00Z"
}
```

## 5. POST /tasks/{task_id}/assign - назначить исполнителя задачи

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| task_id | string | да | ID задачи, для которой назначается исполнитель |

### Request Body

```json
{
  "user_id": "456"
}
```

**Status Codes:**
- `200 OK` - задача изменена
- `400 Bad Request` - неверные параметры запроса
- `404 Not Found` - задача не найдена
- `422 Unprocessable Entity` - неверные типы данных

## 6. POST /tasks/{task_id}/comments - написать комментарий к задаче

### Request Body

| Поле | Тип | Обязательный | Описание |
|------|-----|--------------|----------|
| user_id | string | **да** | ID автора комментария |
| text | string | **да** | Текст комментария (не может быть пустым) |

```json
{
  "id": "501",
  "task_id": "101",
  "user_id": "456",
  "text": "Начал работу над задачей",
  "created_at": "2025-04-15T13:20:00Z"
}
```

**Status Codes:**
- `200 OK` - комментарий добавлен
- `400 Bad Request` - неверные параметры запроса
- `404 Not Found` - задача не найдена
- `422 Unprocessable Entity` - неверные типы данных

### Пример запроса

```json
{
  "user_id": "456",
  "text": "Начал работу над задачей"
}
```

## 7. GET /tasks/{task_id}/comments - получить все комментарии к задаче

### Параметры пути

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| task_id | string | да | ID задачи |

### Status Codes

- `200 OK` - успех
- `404 Not Found` - задача не найдена
- `422 Unprocessable Entity` - неверные типы данных

### Success Response Body (200 OK)

```json
{
  "comments": [
    {
      "id": "501",
      "task_id": "101",
      "user_id": "456",
      "text": "Начал работу над задачей",
      "created_at": "2025-04-15T13:20:00Z"
    },
    {
      "id": "502",
      "task_id": "101",
      "user_id": "123",
      "text": "Хорошо, жду результат",
      "created_at": "2025-04-15T14:00:00Z"
    }
  ]
}
```

## 8. POST /tasks/{task_id}/archive - переместить задачу в архив

### Параметры пути

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| task_id | string | да | ID задачи для архивации |

### Status Codes

- `200 OK` - успех
- `400 OK` - задача уже в архиве
- `404 Not Found` - задача не найдена
- `422 Unprocessable Entity` - неверные типы данных

### Success Response Body (200 OK)

```json
{
  "id": "101",
  "title": "Написать документацию",
  "status": "archived",
  "archived_at": "2025-04-15T15:00:00Z"
}
```

## 9. POST /tasks/{task_id}/summary - получить сводку по задачам

### Status Codes

- `200 OK` - успех
- `422 Unprocessable Entity` - неверные типы данных

### Success Response Body (200 OK)

```json
{
  "total": 25,
  "by_status": {
    "pending": 10,
    "in_progress": 8,
    "completed": 7
  },
  "by_priority": {
    "low": 5,
    "medium": 12,
    "high": 8
  },
  "unassigned": 4
}
```

## 10. GET /tasks/export/ - выгрузить список задач

### Status Codes

- `200 OK` - успех
- `400 OK` - неверный формат
- `422 Unprocessable Entity` - неверные типы данных

### Success Response Body (200 OK) для format=json

```json
[
  {
    "id": "001",
    "title": "Завершить проект",
    "status": "completed",
    "user_id": "123"
  },
  {
    "id": "002",
    "title": "Написать отчет",
    "status": "in_progress",
    "user_id": null
  }
]
```

## Общие статус-коды
| Код | Описание |
|-----|----------|
| 200 | Успех |
| 201 | Создано |
| 400 | Неверный запрос |
| 404 | Не найдено |
| 422 | Необрабатываемый объект |

## Формат ошибок

Все ошибки возвращаются в едином формате:

```json
{
  "error": "ERROR_CODE",
  "message": "Описание ошибки",
  "timestamp": "2025-04-15T10:30:00Z"
}
```

## Примеры запросов с ответами
```bash
curl -X GET "http://api.example.com/tasks?status=completed"
#Response:
{
  "tasks": [
    {
      "id": "001",
      "title": "Завершить проект",
      "description": "Сдать финальную версию",
      "status": "completed",
      "user_id": "123",
      "created_at": "2025-04-10T09:00:00Z",
      "updated_at": "2025-04-14T18:30:00Z"
    }
  ]
} 
```

```bash
curl -X GET "http://api.example.com/tasks/001"
#Response
{
  "id": "001",
  "title": "Завершить проект",
  "description": "Сдать финальную версию клиенту",
  "status": "in_progress",
  "user_id": "123",
  "created_at": "2025-04-10T09:00:00Z",
  "updated_at": "2025-04-14T15:20:00Z"
}
```

```bash
curl -X POST "http://api.example.com/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Написать документацию",
    "description": "Добавить описание всех API методов"
  }'
#Response
{
  "id": "101",
  "title": "Написать документацию",
  "description": "Добавить описание всех API методов",
  "status": "pending",
  "user_id": null,
  "created_at": "2025-04-15T10:30:00Z",
  "updated_at": "2025-04-15T10:30:00Z"
}
```

```bash
curl -X PATCH "http://api.example.com/tasks/101" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Написать финальную документацию",
    "status": "in_progress"
  }'
#Response
{
  "id": "101",
  "title": "Написать финальную документацию",
  "description": "Добавить описание всех API методов",
  "status": "in_progress",
  "user_id": null,
  "created_at": "2025-04-15T10:30:00Z",
  "updated_at": "2025-04-15T11:45:00Z"
}
```

```bash
curl -X POST "http://api.example.com/tasks/101/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "456"
  }'
#Response
{
  "id": "101",
  "title": "Написать документацию",
  "description": "Добавить описание всех API методов",
  "status": "in_progress",
  "user_id": "456",
  "created_at": "2025-04-15T10:30:00Z",
  "updated_at": "2025-04-15T12:00:00Z"
}
```
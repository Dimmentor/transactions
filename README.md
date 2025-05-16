Тесты не писал т.к. не требовалось и не оценивается в ТЗ. Привет принципу YAGNI =) 
Следовало использовать DESIMAL место FLOAT, но думаю не критично для тестового задания.


post - добавление юзера ОК
post - добавление категорий ОК
post - добавление транзакций ОК 
post - добавление транзакций через json ОК 


get - получение списка юзеров ОК
get - получение списка транзакций ОК
get - получение списка транзакций за период ОК


uvicorn app.main:app --port 8000

Проверка категоризации
Добавит категорию Transport
{
    "id": "tx1004",
    "user_id": 1,
    "amount": -1200.0,
    "currency": "RUB",
    "category": null,
    "description": "Taxi from airport",
    "timestamp": "2025-01-18T18:00:00"
  }
Добавит категорию Other
{
    "id": "tx1003",
    "user_id": 1,
    "amount": -1200.0,
    "currency": "RUB",
    "category": null,
    "description": "Something",
    "timestamp": "2025-01-18T18:00:00"
  }

1) Добавление юзера POST http://127.0.0.1:8000/users

{
  "name": "Ivan"
}


2) добавление категорий POST /categories
{
  "name": "Food"
}

3) добавление транзакций POST-запросом: POST /transactions
{
  "id": "tx1001",
  "user_id": 1,
  "amount": -200.0,
  "currency": "RUB",
  "category": "Food",
  "timestamp": "2025-01-16T10:15:00"
}

4) Добавление транзакций POST-запросом, импортируя данные из json-файла:
POST /transactions/import
{
  "file_path": "json/transactions.json"
}

Ответ
{
  "imported": 2
}


5) Запрос списка всех юзеров:
http://127.0.0.1:8000/users
6) Запрос списка всех транзакций 
http://127.0.0.1:8000/transactions
7) Запрос списка транзакций выбранного юзера за период:
GET /users/{user_id}/stats?from=YYYY-MM-DD&to=YYYY-MM-DD
http://127.0.0.1:8000/users/1/stats?from=2025-01-20&to=2025-01-23
8) Запрос списка всех категорий
GET http://127.0.0.1:8000/categories




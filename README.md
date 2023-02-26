# Приложение QRKot
____

Приложение для Благотворительного фонда поддержки котиков.
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.
____

## Технологии:
[Python 3.9](https://www.python.org/downloads/release/python-390/), [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/), [SQLAlchemy](https://www.sqlalchemy.org/)
____

## Как запустить проект(все команды выполняются в командной оболочке bach)

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:VyacheslavRoev/cat_charity_fund.git
```

```
cd cat_charity_fund
```

2. Cоздать и активировать виртуальное окружение:


* Если у вас Linux/macOS

    ```
    python3 -m venv venv
    ```
    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    python -m venv venv
    ```
    ```
    source venv/Scripts/activate
    ```

3. Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
4. В корневой директории создать файл .env с переменными окружения, необходимыми для работы приложения.

```
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
FIRST_SUPERUSER_EMAIL=superuser@user.ru
FIRST_SUPERUSER_PASSWORD=superuser
```

5. Из корневой директории командой uvicorn app.main:app --reload запустить приложение. При первом запуске автоматически будет создан суперюзер с указанными в .env email и паролем
6. Документация API будет доступна по адресам
```
c (здесь же можно авторизоваться и выполнять запросы)
http://127.0.0.1:8000/redoc
 ```
____

## Примеры запросов к API:

Запросить список всех проектов.
```
GET /charity_project/
```
Ответ:
```
[
  {
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2023-02-22T09:29:13.196Z",
    "close_date": "2023-02-22T09:29:13.196Z"
  }
]
```

Создать новый проект. Только для суперюзеров.
```
POST /charity_project/
```
{
  "name": "string",
  "description": "string",
  "full_amount": 0
}
```
Ответ:
```
{
  "name": "string",
  "description": "string",
  "full_amount": 0,
  "id": 0,
  "invested_amount": 0,
  "fully_invested": true,
  "create_date": "2023-02-22T10:53:36.758Z",
  "close_date": "2023-02-22T10:53:36.758Z"
}
```

Удалить проект. Только для суперюзеров.
```
DELETE /charity_project/{project_id}
```
Ответ:
```
{
  "name": "string",
  "description": "string",
  "full_amount": 0,
  "id": 0,
  "invested_amount": 0,
  "fully_invested": true,
  "create_date": "2023-02-22T11:05:35.467Z",
  "close_date": "2023-02-22T11:05:35.467Z"
}
```

Изменить проект. Только для суперюзеров.
```
PATCH /charity_project/{project_id}
```
```{
  "name": "string",
  "description": "string",
  "full_amount": 0
}
```
Ответ:
```
{
  "name": "string",
  "description": "string",
  "full_amount": 0,
  "id": 0,
  "invested_amount": 0,
  "fully_invested": true,
  "create_date": "2023-02-22T11:05:35.467Z",
  "close_date": "2023-02-22T11:05:35.467Z"
}
```

Посмотреть все пожертвования. Только для суперюзеров.
```
GET /donation/
```
Ответ:
```
[
  {
    "full_amount": 0,
    "comment": "string",
    "id": 0,
    "create_date": "2023-02-22T11:12:30.403Z",
    "user_id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "close_date": "2023-02-22T11:12:30.403Z"
  }
]
```

Сделать пожертвование. Для авторизованных.
```
POST /donation/
```
```
{
  "full_amount": 0,
  "comment": "string"
}
```
Ответ:
```
{
  "full_amount": 0,
  "comment": "string",
  "id": 0,
  "create_date": "2023-02-22T11:13:55.634Z"
}
```

Cписок всех пожертвований текущего пользователя.
```
GET /donation/my
```
Ответ:
```
[
  {
    "full_amount": 0,
    "comment": "string",
    "id": 0,
    "create_date": "2023-02-22T11:22:03.890Z"
  }
]
```

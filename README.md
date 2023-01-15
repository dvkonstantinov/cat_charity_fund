# Приложение для благотворительного фонда поддержки 

## Описание проекта
Асинхронный учебный проект на fastapi, pydantic и SQLAlchemy, сервис для благотворителей.

Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

Техническая спецификация приведена в файле ./openapi.json


## Технологический стек
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLALCHEMY](https://www.sqlalchemy.org/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/10.2/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://docs.pydantic.dev/)


## Разворачивание проекта локально (Windows)
1. Скопировать себе гит (git clone)
2. Установить виртуальное окружение
3. Установить зависимости
```
pip install -r requirements.txt
```
4. Выполнить миграции
```
alembic upgrade head
```
5. Создать в корне файл .env:
``` 
APP_TITLE=Приложение QRKot
APP_DESCR=Благотворительный фонд поддержки котиков QRKot
DATABASE_URL=sqlite+aiosqlite:///./charity_fund.db
SECRET=<Секретный код>
FIRST_SUPERUSER_EMAIL=<любой email>
FIRST_SUPERUSER_PASSWORD=<пароль от 3 символов>
```
6. Запускать сервер командой
```
uvicorn app.main:app --reload
```
При первом запуске сервера будет создан суперпользователь с указанным логином-паролем

Swagger будет доступен по ссылке http://127.0.0.1:8000/docs

## Автор
dvkonstantinov
telegram: https://t.me/Dvkonstantinov
# Бэкэнд приложения на Python + FastAPI

Бэкенд (англ. back-end) — начинка сайта или приложения, скрытая от пользователя. Бэкендом называют
часть сервиса, которая работает на сервере, а не в браузере или на компьютере.

В данном примере бэкэнд представляет из себя код для реализации HTTP API для общения с фронтендом.
Для простоты реализации использована популярная библиотека [FastAPI](https://fastapi.tiangolo.com/).


## Зависимости
- `fastapi` – фраемворк для реализации http api интерфейсов
- `pydantic` – библиотека проверки типов данных
- `auth-lib-profcomff[fastapi]` – утилиты для работы с Auth API приложения Твой ФФ
- `SQLAlchemy` – фраемворк для взаимодействия с базами данных
- `psycopg2-binary` – драйвер для подключения к базе данных PostgreSQL
- `alembic` – библиотека для автоматизированного исполнения изменений в базе данных


## Разработка

Для удобства разработки в VS Code создан [workspace](../backend.code-workspace) с преднастроенными
командами и рекомендованными расширениями для работы.

Рекомендуется создать виртуальное окружение для проекта и установить в него зависимости, в том числе
для разработки:

1. Перейдите в папку проекта

2. Создайте виртуальное окружение командой и активируйте его:
    ```console
    foo@bar:~$ python3 -m venv venv
    foo@bar:~$ source ./venv/bin/activate  # На MacOS и Linux
    foo@bar:~$ venv\Scripts\activate  # На Windows
    ```

3. Установите библиотеки
    ```console
    foo@bar:~$ pip install -Ur requirements.txt -r requirements.dev.txt
    ```


## Запуск

1. Перейдите в папку проекта

2. Создайте виртуальное окружение (если оно еще не создано) командой и активируйте его:
    ```console
    foo@bar:~$ python3 -m venv venv
    foo@bar:~$ source ./venv/bin/activate  # На MacOS и Linux
    foo@bar:~$ venv\Scripts\activate  # На Windows
    ```

3. Установите библиотеки
    ```console
    foo@bar:~$ pip install -Ur requirements.txt
    ```

4. Запускайте приложение!
    ```console
    foo@bar:~$ python -m my_app_api
    ```

## ENV-file description
- `DB_DSN=postgresql://postgres@localhost:5432/postgres` – Данные для подключения к БД

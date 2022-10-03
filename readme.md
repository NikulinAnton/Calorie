## Инструкция по разворачиванию локального сервера

1. Создать виртуальное окружение `pipenv --python 3 shell`
2. Установить зависимости `pipenv install` (Если возникнут проблемы с lock файлом, то можно сгенерировать pipfile.lock файл ```pipenv lock``` после чего повторить 2 пункт)
3. Создать .env файл на основе .env.template и заполнить
4. Запустить Docker контейнеры `docker-compose up`
5. Применить миграции `python3 manage.py migrate`

To enable pre-commit hooks run this command:
```pre-commit install```
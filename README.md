# Продуктовая задача ШБР 2023
## Локальный запуск приложения
Для начала нужно установить зависимости:
```console
pip install -r requirements.txt
```
Затем:
```console
make local
```
или
```console
uvicorn main:app --reload
```
эту команду нужно запускать в директории `/app`

Приложение работает по адресу `http://127.0.0.1:8000/`
## Запуск с помощью docker-compose
```console
make docker
```
или
```console
docker-compose up -d --build
```
Приложение работает по адресу `http://127.0.0.1:8080/`
## Запуск тестов
```console
make test
```
или
```console
pytest -v -s tests/
```
## Запуск с помощью docker run
Требуется запущенная база данных PostgresSQL.
Сборка:
```console
docker build . -t app:latest
```
Запуск:
```console
docker run -d --env-file .env-non-dev -p 8080:8080 app
```
## Примечание
Также важно указать переменные окружения для запуска приложения.

`.env` используeтся для локального запуска приложения.

`.env-non-dev` используется для запуска в среде docker.


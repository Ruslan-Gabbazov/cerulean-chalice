# cerulean-chalice

WebSocket-сервер для чата

## Запуск

Создание docker-образа для postgres базы данных:
````
sudo docker volume create postgres-data
sudo docker run -e POSTGRES_PASSWORD=password -e POSTGRES_USER=rest -p 5432:5432 --name postgres --mount source=postgres-data,target=/var/lib/postgresql  -d postgres:11

sudo docker exec -it postgres psql -U rest
````
Создание базы данных внутри образа:
````
CREATE DATABASE chat;
GRANT ALL PRIVILEGES ON DATABASE chat TO rest;
\q
````
Перейти в желаемую директорию.

Клонирование репозитория:
````
git clone https://github.com/Ruslan-Gabbazov/cerulean-chalice.git
cd ./cerulean-chalice
````
Запуск сервера:
````
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python3 main.py
````

Сервер будет доступен по адресу: http://127.0.0.1:8080/

Подключение клиента через: http://127.0.0.1:8080/connect

## Взаимодействие

Общение сервера с клиентом происходит в следующем формате:
````
{
    "kind": "",
    "payload": {}
}
````

События от сервера:
````
"kind": 'initial'
"kind": 'authorize'
"kind": 'send'
"kind": 'remove'
````

События от клиента:
````
"kind": 'ping'
"kind": 'signin'
"kind": 'signup'
"kind": 'message'
"kind": 'disconnect'
````

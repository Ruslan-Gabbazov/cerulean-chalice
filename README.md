# cerulean-chalice

---  
Веб-чат на WebSocket

## Стек

---
<img src="https://img.shields.io/badge/Python-8F8FA6?style=for-the-badge&logo=Python&logoColor=#3776AB"/>
<img src="https://img.shields.io/badge/aiohttp-8F8FA6?style=for-the-badge&logo=aiohttp&logoColor=2C5BB4"/>
<img src="https://img.shields.io/badge/PostgreSQL-8F8FA6?style=for-the-badge&logo=PostgreSQL&logoColor=4169E1"/>
<img src="https://img.shields.io/badge/Alchemy-8F8FA6?style=for-the-badge&logo=Alchemy&logoColor=0C0C0E"/>

####

<img src="https://img.shields.io/badge/HTML5-8F8FA6?style=for-the-badge&logo=HTML5&logoColor=E34F26"/>  
<img src="https://img.shields.io/badge/CSS3-8F8FA6?style=for-the-badge&logo=CSS3&logoColor=1572B6"/>  
<img src="https://img.shields.io/badge/JavaScript-8F8FA6?style=for-the-badge&logo=JavaScript&logoColor=F7DF1E"/>

## Сервер

---
#### Создание docker-образа для postgres базы данных:
````
sudo docker volume create postgres-data
sudo docker run -e POSTGRES_PASSWORD=password -e POSTGRES_USER=rest -p 5432:5432 --name postgres --mount source=postgres-data,target=/var/lib/postgresql  -d postgres:11

sudo docker exec -it postgres psql -U rest
````
#### Создание базы данных внутри образа:
````
CREATE DATABASE chat;
GRANT ALL PRIVILEGES ON DATABASE chat TO rest;
\q
````
Перейти в желаемую директорию.

#### Клонирование репозитория:
````
git clone https://github.com/Ruslan-Gabbazov/cerulean-chalice.git
cd ./cerulean-chalice
````
#### Запуск сервера:
````
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python3 main.py
````
Сервер будет расположен по адресу: ```http://127.0.0.1:8080/```

## Клиент

---
Достаточно открыть файл ```./client/index.html```  
Подключение клиента к серверу происходит через: ```http://127.0.0.1:8080/connect```

## Взаимодействие

---
#### Общение сервера с клиентом происходит в следующем формате:
````
{
    "kind": "",
    "payload": {
        "connection_id": "",
        "nickname": "",
        "password": "",
        "allowed": "",
        "content": ""
    }
}
````

#### События от сервера:
````
"kind": 'initial'
"kind": 'authorize'
"kind": 'send'
"kind": 'remove'
````

#### События от клиента:
````
"kind": 'ping'
"kind": 'signin'
"kind": 'signup'
"kind": 'authorized'
"kind": 'message'
"kind": 'disconnect'
````

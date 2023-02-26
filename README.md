# cerulean-chalice

WebSocket-сервер для чата

## Запуск

````
py -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
````

Сервер: http://127.0.0.1:8080/

## Взаимодействие

Общение сервера с клиентом происходит в слейдующем формате:
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

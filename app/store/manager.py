import typing
from datetime import datetime
from dataclasses import asdict

from app.chat.models import User, Event, Message
from app.database.db_accessor import DBAccessor
from app.store.accessor import BaseAccessor
from app.store.events import ClientEventKind, ServerEventKind

if typing.TYPE_CHECKING:
    from app.store.store import Store


class Manager(BaseAccessor):
    class Meta:
        name = 'manager'

    def __init__(self, store: 'Store'):
        super().__init__(store)
        self.db_accessor: DBAccessor = DBAccessor(store)
        self._current_users: dict[str, User] = {}

    async def handle_event(self, event: Event):
        connection_id = event.payload['connection_id']

        match event.kind:
            case ClientEventKind.PING_EVENT:
                await self.on_ping(connection_id)
            case ClientEventKind.SIGNUP_EVENT:
                await self.on_signup(connection_id, event.payload)
            case ClientEventKind.SIGNIN_EVENT:
                await self.on_signin(connection_id, event.payload)
            case ClientEventKind.MESSAGE_EVENT:
                await self.on_message(connection_id, event.payload)
            case ClientEventKind.DISCONNECT_EVENT:
                await self.on_disconnect(connection_id)
            case _:
                raise NotImplementedError(event.kind)

    async def handle_open(self, connection_id: str):
        self.logger.info(f'Open connection: {connection_id}')
        await self.store.ws.push(
            connection_id,
            event=Event(
                kind=ServerEventKind.INITIAL,
                payload={
                    'connection_id': connection_id,
                }
            )
        )

    async def handle_close(self, connection_id: str):
        await self.on_disconnect(connection_id)

    async def on_signup(self, connection_id: str, payload: dict):
        user = User(nickname=payload['nickname'],
                    password=payload['password']
                    )
        user_id = await self.db_accessor.add_user(user)
        user.user_id = user_id
        self._current_users[connection_id] = user

        await self._authorize(connection_id, True)
        all_messages = await self.db_accessor.get_all_messages()
        await self.send_all(connection_id, all_messages)

    async def on_signin(self, connection_id: str, payload: dict):
        user = User(nickname=payload['nickname'],
                    password=payload['password']
                    )
        (allowed, user_id) = await self.db_accessor.check_user_and_get_id(user)
        await self._authorize(connection_id, allowed)

        if allowed:
            user.user_id = user_id
            self._current_users[connection_id] = user
            all_messages = await self.db_accessor.get_all_messages()
            await self.send_all(connection_id, all_messages)

    async def _authorize(self, connection_id: str, allowed: bool):
        self.logger.info(f'Authorization of connection: {connection_id} - {allowed=}')
        await self.store.ws.push(
            connection_id=connection_id,
            event=Event(
                kind='authorize',
                payload={'connection_id': connection_id,
                         'allowed': allowed})
        )

    async def on_message(self, connection_id, payload: dict):
        self.logger.info(f'Receive message from connection: {connection_id}')
        message = Message(
            user_id=self._current_users[connection_id].user_id,
            content=payload['content'],
            datetime=str(datetime.now())
        )

        message_id = await self.db_accessor.add_message(message)
        message.message_id = message_id
        await self.send_all(connection_id, [message])

    async def send_all(self, connection_id: str, messages: list[Message]):
        self.logger.info(f'Close connection: {connection_id}')
        await self.store.ws.push_all(
            event=Event(
                kind=ServerEventKind.SEND,
                payload={'connection_id': connection_id,
                         'messages': [asdict(message) for message in messages if message]})
        )

    async def on_ping(self, connection_id: str):
        self.logger.info(f'Ping connection: {connection_id}')

    async def on_disconnect(self, connection_id: str):
        try:
            self._current_users.pop(connection_id)
        except KeyError:
            pass

        await self.store.ws.push_all(
            event=Event(
                kind=ServerEventKind.REMOVE,
                payload={'connection_id': connection_id})
        )
        self.logger.info(f'Close connection: {connection_id}')

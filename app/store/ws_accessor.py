import asyncio
import json
import typing
import uuid
from asyncio import Task
from dataclasses import asdict
from typing import Any

from aiohttp.web_ws import WebSocketResponse
from app.store.accessor import BaseAccessor
from app.chat.models import Event

if typing.TYPE_CHECKING:
    from app.chat.app import Request
    from app.store.store import Store


class WSAccessor(BaseAccessor):
    class Meta:
        name = 'ws'

    CONNECTION_TIMEOUT = 100

    def __init__(self, store: 'Store'):
        super().__init__(store)
        self._connections: dict[str, Any] = {}  # Any -> WebSocketResponse()
        self._timeout_tasks: dict[str, Task] = {}

    async def handle_request(self, request: 'Request') -> WebSocketResponse:
        response = WebSocketResponse()
        await response.prepare(request)
        connection_id = str(uuid.uuid4())
        self._connections[connection_id] = response

        self._timeout_refresh(connection_id)
        await self.store.manager.handle_open(connection_id)
        await self.read(connection_id)
        await self.close(connection_id)

        return response

    async def read(self, connection_id: str):
        async for message in self._connections[connection_id]:
            self._timeout_refresh(connection_id)
            raw_event = json.loads(message.data)
            await self.store.manager.handle_event(
                event=Event(
                    kind=raw_event['kind'],
                    payload=raw_event['payload'],)
                )

    async def close(self, connection_id: str):
        connection = self._connections.pop(connection_id)
        await self.store.manager.on_disconnect()
        await connection.close()

    async def push(self, connection_id: str, event: Event):
        json_data = json.dumps(asdict(event))
        await self._push(connection_id, json_data)

    async def push_all(self, event: Event):
        json_data = json.dumps(asdict(event))
        ops = [self._push(connection_id, json_data) for connection_id in self._connections.keys()]
        await asyncio.gather(*ops, return_exceptions=True)

    async def _push(self, connection_id: str, data: str):
        await self._connections[connection_id].send_str(data)

    def _timeout_refresh(self, connection_id: str):
        self.logger.info(f'Refresh timeout of connection: {connection_id}')
        task = self._timeout_tasks.get(connection_id)
        if task:
            task.cancel()

        task = asyncio.create_task(self._timeout_disconnect(connection_id))
        self._timeout_tasks[connection_id] = task

    async def _timeout_disconnect(self, connection_id: str):
        await asyncio.sleep(self.CONNECTION_TIMEOUT)
        self.logger.info(f'Timeout of connection: {connection_id}')
        await self.store.manager.handle_close(connection_id)
        await self.store.ws.close(connection_id)

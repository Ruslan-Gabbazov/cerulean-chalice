import os
from aiohttp.web import Response
from app import BASE_DIR
from app.chat.app import View


class IndexView(View):
    @staticmethod
    async def get():
        with open(os.path.join(BASE_DIR, 'client', 'static', 'templates', 'index.html'), 'r') as f:
            file = f.read()

        return Response(body=file, headers={'Content-Type': 'text/html', })


class ChatView(View):
    @staticmethod
    async def get(self):
        with open(os.path.join(BASE_DIR, 'client', 'static', 'templates', 'chat.html'), 'r') as f:
            file = f.read()

        return Response(body=file, headers={'Content-Type': 'text/html', })


class WSConnectView(View):
    async def get(self):
        ws = await self.store.ws.handle_request(self.request)
        return ws

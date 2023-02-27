from app.chat.app import View


class WSConnectView(View):
    async def get(self):
        ws = await self.store.ws.handle_request(self.request)
        return ws

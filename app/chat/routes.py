import os
import typing
from app import BASE_DIR

if typing.TYPE_CHECKING:
    from app.chat.app import Application


def setup_routes(app: 'Application'):
    from app.chat.views import WSConnectView, IndexView, ChatView

    app.router.add_view('/connect', WSConnectView)
    app.router.add_static("/static", os.path.join(BASE_DIR, "client", "static"))
    app.router.add_view("/", IndexView)
    app.router.add_view("/chat", ChatView)

from aiohttp.web_app import Application
from app.chat.routes import setup_routes as chat_setup_routes


def setup_routes(app: Application):
    chat_setup_routes(app)

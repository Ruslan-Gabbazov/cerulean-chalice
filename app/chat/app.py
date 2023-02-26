import typing
import logging
import aiohttp.web as web
from app.store.store import Store
from app.chat.routes import setup_routes


class Application(web.Application):
    database: dict = {'users': [],
                      'messages': []}  # ?
    store: "Store"
    logger: typing.Optional[logging.Logger] = None


class Request(web.Request):
    @property
    def app(self) -> Application:
        return super().app()


class View(web.View):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def app(self) -> "Application":
        return self.request.app

    @property
    def store(self) -> "Store":
        return self.app.store


def setup_app():
    app = Application()

    logging.basicConfig(level=logging.INFO)
    app.logger = logging.getLogger()

    app.store = Store(app)
    setup_routes(app)
    return app

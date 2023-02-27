import typing
import logging
import aiohttp.web as web

from app.store.store import Store
from app.database.accessor import Database
from app.chat.routes import setup_routes
from app.settings import config


class Application(web.Application):
    store: "Store"
    database: typing.Optional[Database] = None
    logger: typing.Optional[logging.Logger] = None
    config: dict = config


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

    app.database = Database(app)
    app.database.setup_db(app)

    app.store = Store(app)
    setup_routes(app)
    return app

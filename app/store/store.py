import typing

from app.store.ws_accessor import WSAccessor
from app.store.manager import Manager

if typing.TYPE_CHECKING:
    from app.chat.app import Application


class Store:
    def __init__(self, app: "Application"):
        self.app = app
        self.ws = WSAccessor(self)
        self.manager = Manager(self)

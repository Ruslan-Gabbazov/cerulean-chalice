import typing

if typing.TYPE_CHECKING:
    from app.store.store import Store


class BaseAccessor:
    class Meta:
        name = 'base_accessor'

    def __init__(self, store: 'Store'):
        self.app = store.app
        self.store = store
        self.logger = store.app.logger.getChild(self.Meta.name)

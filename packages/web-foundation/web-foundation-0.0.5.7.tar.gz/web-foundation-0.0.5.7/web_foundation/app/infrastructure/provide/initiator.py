from typing import TypeVar, Generic

from web_foundation.app import App
from web_foundation.app.infrastructure.provide.provider import Provider
from web_foundation.kernel import NamedContext

InitableApp = TypeVar('InitableApp', bound=App, contravariant=True)


class Initiator(Generic[InitableApp]):
    app: InitableApp
    close_event_name = "finalize_init"

    def __init__(self, app: InitableApp):
        self.app = app
        Provider.reg(app.name, self)
        pass

    async def close(self):
        raise NotImplementedError

    async def setup_connection(self, named_ctx: NamedContext | None = None):
        raise NotImplementedError

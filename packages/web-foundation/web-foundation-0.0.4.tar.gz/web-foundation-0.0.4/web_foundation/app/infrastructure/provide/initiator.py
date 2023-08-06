from web_foundation.app.infrastructure.provide.provider import Provider
from web_foundation.kernel import NamedContext


class Initiator:
    app: "App"
    close_event_name = "finalize_init"

    def __init__(self, app: "App"):
        self.app = app
        Provider.reg(app.name, self)
        pass

    async def close(self):
        raise NotImplementedError

    async def setup_connection(self, named_ctx: NamedContext | None = None):
        raise NotImplementedError

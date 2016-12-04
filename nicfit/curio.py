import curio
from .app import AsyncApplication


class Application(AsyncApplication):
    with_monitor = True

    def _run(self):
        curio.run(self.main(), with_monitor=Application.with_monitor)

import curio
from .app import AsyncApplication


class Application(AsyncApplication):
    with_monitor = True

    def _run(self, args_list=None):
        retval = curio.run(self.main(args_list=args_list),
                           with_monitor=Application.with_monitor)
        return retval

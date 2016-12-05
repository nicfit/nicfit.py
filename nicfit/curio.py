import curio
from .app import AsyncApplication


class Application(AsyncApplication):
    def __init__(self, main_func=None, *, with_monitor=False, **kwargs):
        super().__init__(main_func, **kwargs)
        self._monitor = with_monitor

    def _run(self, args_list=None):
        self.log.debug("curio.Application: {args_list}".format(**locals()))
        retval = curio.run(self.main(args_list=args_list),
                           with_monitor=self._monitor)
        return retval

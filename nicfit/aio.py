import asyncio
from .app import AsyncApplication


class Application(AsyncApplication):

    def __init__(self, main_func=None, *, event_loop=None, **kwargs):
        super().__init__(main_func, **kwargs)
        self.event_loop = event_loop or asyncio.get_event_loop()
        self._main_task = None
        self._exit_status = None

    def _run(self, args_list=None):
        self.log.debug("aio.Application: {args_list}".format(**locals()))
        self._main_task = \
            self.event_loop.create_task(self.main(args_list=args_list))
        try:
            self._exit_status = \
                self.event_loop.run_until_complete(self._main_task)
        except asyncio.CancelledError as ex:
            self.log.debug("aio.Application: Cancelled: {}"
                           .format(ex))
        return self._exit_status

    def stop(self, exit_status=0):
        self.log.debug("Application::stop(exit_status=%d)" % exit_status)
        self._exit_status = exit_status
        self._main_task.cancel()

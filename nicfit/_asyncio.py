import asyncio
from .app import AsyncApplication


class Application(AsyncApplication):

    def __init__(self, main_func=None, *, event_loop=None, **kwargs):
        super().__init__(main_func, **kwargs)
        self.event_loop = event_loop or asyncio.get_event_loop()

    def _run(self):
        main_task = self.event_loop.create_task(self.main())
        retval = self.event_loop.run_until_complete(main_task)
        return retval

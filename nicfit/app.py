import sys
from ._argparse import ArgumentParser
from ._logging import getLogger

log = getLogger(__name__)


class Application:
    UNCAUGHT_EXCEPTION_EXIT = 126
    NO_MAIN_EXIT = 127

    def _main(self, args):
        """
        Subclasses should implement, or pass main_func top the constructor.
        """
        self.log.debug("Application._main: {args}".format(**locals()))
        assert args is self.args
        if self._main_func:
            return self._main_func(args)
        return Application.NO_MAIN_EXIT

    def _atexit(self):
        """Invoked in the 'finally' block of Application.run."""
        self.log.debug("Application._atexit")
        if self._atexit_func:
             self._atexit_func(self)

    def __init__(self, main_func=None, *, name=None,
                 logging_args=True, config_opts=None, atexit=None):
        self.name = name
        self._main_func = main_func
        self._atexit_func = atexit
        self.arg_parser = ArgumentParser(prog=name, add_log_args=logging_args,
                                         config_opts=config_opts)
        self.arg_parser.set_defaults(app=self)
        self.log = getLogger(name) if name else log

    def main(self, args_list=None):
        self.log.debug("Application.main: {args_list}".format(**locals()))
        self.args = self.arg_parser.parse_args(args=args_list)
        retval = self._main(self.args)
        return retval or 0

    def run(self, args_list=None):
        """Run Application.main and exits with the return value."""
        self.log.debug("Application.run: {args_list}".format(**locals()))
        retval = None
        try:
            retval = self._run(args_list=args_list)
        except KeyboardInterrupt:
            self.log.verbose("Interrupted")
        except Exception as ex:
            retval = Application.UNCAUGHT_EXCEPTION_EXIT
            self.log.exception("Uncaught exception")
            raise
        finally:
            try:
                self._atexit()
            finally:
                sys.exit(retval)

    def _run(self, args_list=None):
        self.log.debug("Application._run: {args_list}".format(**locals()))
        return self.main(args_list=args_list)


class AsyncApplication(Application):
    async def _main(self, args):
        self.log.debug("AsyncApplication._main: {args}".format(**locals()))
        if self._main_func:
            return await self._main_func(args)
        return self.NO_MAIN_EXIT

    async def main(self, args_list=None):
        self.log.debug("AsyncApplication: {args_list}".format(**locals()))
        self.args = self.arg_parser.parse_args(args=args_list)
        retval = await self._main(self.args)
        return retval or 0

    def _run(self):
        raise NotImplementedError("Implemement for a specific async API")

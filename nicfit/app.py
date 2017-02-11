import sys
import logging

from ._logging import getLogger
from ._argparse import ArgumentParser
from .util import initGetText

log = getLogger(__name__)

try:
    import ipdb as _debugger
except ImportError:                                            # pragma: nocover
    import pdb as _debugger
def _pdb():  # noqa: E302
    e, m, tb = sys.exc_info()
    _debugger.post_mortem(tb)


class Application:
    UNCAUGHT_EXCEPTION_EXIT = 126
    NO_MAIN_EXIT = 127

    def __init__(self, main_func=None, *, name=None, description=None,
                 logging_args=True, config_opts=None, version=None,
                 atexit=None, pdb_opt=False, extra_arg_parser_opts=None,
                 gettext_domain=None):
        self._main_func = main_func
        self._atexit_func = atexit

        self.log = getLogger(name) if name else log
        logging.basicConfig()

        extra_arg_parser_opts = extra_arg_parser_opts or {}
        parser = ArgumentParser(add_log_args=logging_args,
                                config_opts=config_opts,
                                prog=name, description=description,
                                **extra_arg_parser_opts)
        self.name = parser.prog

        if version:
            parser.add_argument("--version", action="version", version=version)
        if pdb_opt:
            parser.add_argument("--pdb", action="store_true", dest="debug_pdb",
                                help="Drop into 'pdb' for unhandled exceptions")

        parser.set_defaults(app=self)
        self.arg_parser = self._addArguments(parser) or parser

        if gettext_domain:
            translation = initGetText(gettext_domain, install=True)
            if translation is None:
                raise ValueError("Unable to find gettext message catalog for "
                                 "gettext_domain='{}'".format(gettext_domain))
            self.translation = translation

    def _main(self, args):
        """
        Subclasses should implement, or pass main_func to the constructor.
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

    def _addArguments(self, parser):
        return parser

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
            self.log.verbose("Interrupted")                    # pragma: nocover
        except SystemExit as exit:
            self.log.verbose("Exited")
            retval = exit.code
        except Exception as ex:
            if "debug_pdb" in self.args and self.args.debug_pdb:
                _pdb()
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

    def enableCommands(self, title="Commands", description=None,
                       add_help_subcmd=True, dest="command"):
        from .command import Command
        subs = self.arg_parser.add_subparsers(title=title,
                                              description=description,
                                              add_help_subcmd=add_help_subcmd,
                                              dest=dest)
        Command.initAll(subs)
        return subs


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

    def _run(self, args_list=None):
        raise NotImplementedError("Implemement for a specific async API")

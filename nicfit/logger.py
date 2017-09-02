import sys
import time
import argparse
import logging
import logging.config
from io import StringIO
from .deprecation import deprecated
#from deprecation import deprecated


class Logger(logging.getLoggerClass()):
    """Base class for all package loggers"""

    def __init__(self, name):
        super().__init__(name)

        # Using propogation of child to parent, by default
        self.propagate = True
        self.setLevel(logging.NOTSET)

    def verbose(self, msg, *args, **kwargs):
        """Log msg at 'verbose' level, debug < verbose < info"""
        self.log(logging.VERBOSE, msg, *args, **kwargs)


def getLogger(name=None):
    OrigLoggerClass = logging.getLoggerClass()
    try:
        logging.setLoggerClass(Logger)
        return logging.getLogger(name)
    finally:
        logging.setLoggerClass(OrigLoggerClass)


def _initConsoleLogger(name, level, handler=None):
    handler = handler or logging.StreamHandler(sys.stdout)
    l = getLogger(name)
    l.propagate = False
    l.setLevel(level)
    l.addHandler(handler)
    return l


stdout = _initConsoleLogger("_stdout", logging.DEBUG,
                            logging.StreamHandler(sys.stdout))
stderr = _initConsoleLogger("_stderr", logging.WARNING,
                            logging.StreamHandler(sys.stderr))
try:
    import logging_spinner
    progress = _initConsoleLogger(
        "_progress", logging.DEBUG,
        logging_spinner.SpinnerHandler(stream=sys.stdout))
except ImportError:
    progress = None

LOG_FORMAT = "[%(asctime)s] %(name)-25s [%(levelname)-8s]: %(message)s"

logging.VERBOSE = logging.DEBUG + ((logging.INFO - logging.DEBUG) // 2)
logging.addLevelName(logging.VERBOSE, "VERBOSE")
LEVELS = [logging.DEBUG, logging.VERBOSE, logging.INFO,
          logging.WARNING, logging.ERROR, logging.CRITICAL]
LEVEL_NAMES = [logging.getLevelName(l).lower() for l in LEVELS]


def _optSplit(opt):
    if ':' in opt:
        first, second = opt.split(":", maxsplit=1)
    else:
        first, second = None, opt
    return first or None, second or None


def addCommandLineArgs(arg_parser):
    """Add logging option to an ArgumentParser."""
    arg_parser.register("action", "log_levels", LogLevelAction)
    arg_parser.register("action", "log_files", LogFileAction)
    arg_parser.register("action", "log_help", LogHelpAction)

    group = arg_parser.add_argument_group("Logging options")
    group.add_argument(
        "-l", "--log-level", dest="log_levels",
        action="log_levels", metavar="LOGGER:LEVEL", default=[],
        help="Set log levels for individual loggers. See --help-logging for "
             "complete details.")

    group.add_argument(
        "-L", "--log-file", dest="log_files",
        action="log_files", metavar="LOGGER:FILE", default=[],
        help="Set log the output file for individual loggers. "
             " See --help-logging for complete details.")

    group.add_argument("--help-logging", action="log_help",
                       help=argparse.SUPPRESS)


def applyLoggingOpts(log_levels, log_files):
    """Apply logging options produced by LogLevelAction and LogFileAction.

    More often then not this function is not needed, the actions have already
    been taken during the parse, but it can be used in the case they need to be
    applied again (e.g. when command line opts take precedence but were
    overridded by a fileConfig, etc.).
    """
    for l, lvl in log_levels:
        l.setLevel(lvl)
    for l, hdl in log_files:
        for h in l.handlers:
            l.removeHandler(h)
        l.addHandler(hdl)


class LogLevelAction(argparse._AppendAction):
    """An 'action' value for log level setting options."""
    def __call__(self, parser, namespace, values, option_string=None):
        log_name, log_level = _optSplit(values)

        if log_level.lower() not in LEVEL_NAMES:
            raise ValueError("Unknown log level: {}".format(log_level))

        logger, level = (logging.getLogger(log_name),
                         getattr(logging, log_level.upper()))
        logger.setLevel(level)

        values = tuple([logger, level])
        super().__call__(parser, namespace, values, option_string=option_string)


class LogFileAction(argparse._AppendAction):
    """An 'action' value for log file setting options."""
    def __call__(self, parser, namespace, values, option_string=None):
        log_name, logpath = _optSplit(values)

        logger, logpath = logging.getLogger(log_name), logpath

        formatter = None
        handlers_logger = None
        if logger.hasHandlers():
            # Find the logger with the actual handlers attached
            handlers_logger = logger if logger.handlers else logger.parent
            while not handlers_logger.handlers:
                handlers_logger = handlers_logger.parent

            assert(handlers_logger)
            for h in list(handlers_logger.handlers):
                formatter = h.formatter
                handlers_logger.removeHandler(h)
        else:
            handlers_logger = logger

        if logpath in ("stdout", "stderr"):
            h = logging.StreamHandler(stream=sys.stdout if "out" in logpath
                                                        else sys.stderr)
        elif logpath == "null":
            h = logging.NullHandler()
        else:
            h = logging.FileHandler(logpath)

        h.setFormatter(formatter)
        handlers_logger.addHandler(h)
        handlers_logger.propagate = False

        values = tuple([logger, h])
        super().__call__(parser, namespace, values, option_string=option_string)


class LogHelpAction(argparse._HelpAction):
    def __call__(self, parser, namespace, values, option_string=None):
        print(_LOGGING_OPTS_HELP)
        parser.exit()


def DEFAULT_LOGGING_CONFIG(level=logging.WARN, format=LOG_FORMAT):
    """Returns a default logging config in dict format.

     Compatible with logging.config.dictConfig(), this default set the root
     logger to `level` with `sys.stdout` console handler using a formatter
     initialized with `format`. A simple 'brief' formatter is defined that
     shows only the message portion any log entries."""
    return {
        "formatters": {"generic": format,
                       "brief": "%(message)s",
                      },
        "handlers": {"console": {"class": "logging.StreamHandler",
                                 "level": "NOTSET",
                                 "formatter": "generic",
                                 "stream": "ext://sys.stdout",
                                },
                    },
        "root": {"level": level,
                 "handlers": ["console"],
                },
        "loggers": {},
    }


def PKG_LOGGING_CONFIG(pkg_logger, propagate=True, pkg_level=logging.NOTSET):
    return {pkg_logger: {"level": pkg_level,
                         "propagate": propagate,
                        }
           }


@deprecated("Foo")
def LOGGING_CONFIG(pkg_logger, root_level="WARN", log_format=LOG_FORMAT,
                   pkg_level="NOTSET", init_logging=False):
    cfg = """
###
#logging configuration
#https://docs.python.org/3/library/logging.config.html#configuration-file-format
###

[loggers]
keys = root, {pkg_logger}

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = {root_level}
handlers = console

[logger_{pkg_logger}]
level = {pkg_level}
qualname = {pkg_logger}
; When adding more specific handlers than what exists on the root you'll
; likely want to set propagate to false.
handlers =
propagate = 1

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = {log_format}

""".format(**locals())
    if init_logging:
        logging.config.fileConfig(StringIO(cfg))
    return cfg


_LOGGING_OPTS_HELP = """
The command line options ``-l (--log-level)`` and ``-L (--log-file)`` can be
used to set levels and output streams for any and all loggers, therefore each
may be specified multiple times on a command line.

Each argument requires a value of the form ``VALUE`` or ``LOGGER:VALUE``.
When a LOGGER is not specified the VALUE is applied to the root logger.

Valid level names (-l and --log-level) are:
{level_names}

Note, nicfit.py loggers add a VERBOSE level, where DEBUG < VERBOSE < INFO.

Valid log file values (-L and --log-file) are any file path with the required
permissions to open and write to the file. The special values 'stdout',
'stderr', and 'null' result on logging to the console (stdout or stderr),
or /dev/null in the last case.

For example:

example.py -l info -l mylib:debug -l mylib.database:critical -L ./info.log -L mylib:./debug.log -L mylib.database:/dev/stderr

""".format(level_names=", ".join(LEVEL_NAMES))  # noqa


__all__ = ["stdout", "stderr"]


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    for log in stdout, stderr:
        print("root L:", logging.getLogger().getEffectiveLevel())
        print("nicfit L:", logging.getLogger("nicfit").getEffectiveLevel())
        print("L:", log.getEffectiveLevel())
        log.debug(str((log, "debug")))
        log.verbose(str((log, "verbose")))
        log.info(str((log, "info")))
        log.warning(str((log, "warning")))
        log.error(str((log, "error")))
        log.critical(str((log, "critical")), extra={"user_waiting": False})

    if progress:
        progress.debug("Doing shit...", extra={'user_waiting': True})
        time.sleep(2)
        progress.debug("Still doing shit...", extra={'user_waiting': True})
        time.sleep(3)
        progress.debug("Almost done doing shit..", extra={'user_waiting': True})
        time.sleep(2)
        progress.debug("Done doing shit...", extra={'user_waiting': False})

# -*- coding: utf-8 -*-
import sys
import logging
import logging.config
import argparse
from io import StringIO

"""
TODO
"""

LOG_FORMAT = "[%(asctime)s] %(name)-25s [%(levelname)-8s]: %(message)s"
METRICS_FORMAT = "<metrics time='%(asctime)s'>%(message)s</metrics>"

logging.VERBOSE = logging.DEBUG + ((logging.INFO - logging.DEBUG) // 2)
logging.addLevelName(logging.VERBOSE, "VERBOSE")
LEVELS = [logging.DEBUG, logging.VERBOSE, logging.INFO,
          logging.WARNING, logging.ERROR, logging.CRITICAL]
LEVEL_NAMES = [logging.getLevelName(l).lower() for l in LEVELS]


def getLogger(name):
    OrigLoggerClass = logging.getLoggerClass()
    try:
        logging.setLoggerClass(Logger)
        return logging.getLogger(name)
    finally:
        logging.setLoggerClass(OrigLoggerClass)


class Logger(logging.getLoggerClass()):
    '''Base class for all package loggers'''

    def __init__(self, name):
        super().__init__(name)

        # Using propogation of child to parent, by default
        self.propagate = True
        self.setLevel(logging.NOTSET)

    def verbose(self, msg, *args, **kwargs):
        '''Log \a msg at 'verbose' level, debug < verbose < info'''
        self.log(logging.VERBOSE, msg, *args, **kwargs)


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

    group = arg_parser.add_argument_group("Logging options")
    group.add_argument(
        "-l", "--log-level", dest="log_levels",
        action="log_levels", metavar="LOGGER:LEVEL", default=[],
        help="Set logging levels (the option may be specified multiple "
             "times). The level of a specific logger may be set with "
             "the syntax LOGGER:LEVEL, but LOGGER is optional so "
             "if only LEVEL is given it applies to the root logger. "
             "Valid level names are: %s" % ", ".join(LEVEL_NAMES))

    group.add_argument(
        "-L", "--log-file", dest="log_files",
        action="log_files", metavar="LOGGER:FILE", default=[],
        help="Set log files (the option may be specified multiple "
             "times). The level of a specific logger may be set with "
             "the syntax LOGGER:FILE, but LOGGER is optional so "
             "if only FILE is given it applies to the root logger. "
             "The special FILE values 'stdout', 'stderr', and 'null' "
             "result on logging to the console, or /dev/null in the "
             "latter case.")


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

        values = tuple([logger, h])
        super().__call__(parser, namespace, values, option_string=option_string)


# FIXME: metrics does not really belong in generic version
def LOGGING_CONFIG(pkg_logger, root_level="WARN", log_format=LOG_FORMAT,
                   pkg_level="NOTSET", metrics_format=METRICS_FORMAT,
                   init_logging=False):
    cfg = """
###
#logging configuration
#https://docs.python.org/3/library/logging.config.html#configuration-file-format
###

[loggers]
keys = root, {pkg_logger}, {pkg_logger}.metrics

[handlers]
keys = console, metrics

[formatters]
keys = generic, metrics

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

[logger_{pkg_logger}.metrics]
level = NOTSET
qualname = {pkg_logger}.metrics
handlers = metrics
propagate = 0

[handler_metrics]
class = FileHandler
args = ("{pkg_logger}-metrics.log", "w", None, True)
level = NOTSET
formatter = metrics

[formatter_metrics]
format = {metrics_format}

""".format(**locals())
    if init_logging:
        logging.config.fileConfig(StringIO(cfg))
    return cfg

# -*- coding: utf-8 -*-
import argparse
import configparser
from io import StringIO
from pathlib import Path

DEFAULT_CONFIG = None


class Config(configparser.ConfigParser):
    '''Class for storing, reading, and writing config.'''
    def __init__(self, filename, **kwargs):
        super().__init__(**kwargs)
        self.filename = Path(filename)


class ConfigFileType(argparse.FileType):
    '''ArgumentParser ``type`` for loading ``Config`` objects.'''
    def __init__(self, default_config=None, encoding="utf-8"):
        super().__init__(mode='r')
        self._encoding = encoding
        self._default_config = default_config

    def __call__(self, filename):
        try:
            fp = super().__call__(filename)
        except Exception as ex:
            if self._default_config:
                fp = StringIO(self._default_config)
            else:
                raise

        config = Config(filename)
        config.readfp(fp)

        return config


def addCommandLineArgs(arg_parser, required=False, default_file=None,
                       default_config=DEFAULT_CONFIG):
    group = arg_parser.add_argument_group("Configuration options")
    if required:
        arg_parser.add_argument("config", default=default_file,
                          help="Configuration file (ini file format).",
                          type=ConfigFileType(default_config=DEFAULT_CONFIG),
                          nargs="?" if default_file else None)
    else:
        group.add_argument("-c", "--config", dest="config",
                           metavar="FILENAME",
                           type=ConfigFileType(default_config=DEFAULT_CONFIG),
                           default=default_file,
                           help="Configuration file (ini file format).")

    # FIXME: implement the subs
    group.add_argument("-o", dest="config_overrides", action="append",
                       default=[], metavar="SECTION:OPTION=VALUE",
                       help="Overrides the values for configuration OPTION in "
                            "[SECTION].")


## THis is the old arg parser with config built in
'''
class ArgumentParser(argparse.ArgumentParser):
    """
    A subclased of argparse.ArgumentParser with added support for logging and
    config file arguments.

    -l debug
    -llogger:warn
    --log-level log2:error

    TODO
    FIXME
    """

    def __init__(self, add_log_args=False, config_opts=None, **kwargs):
        self._config_opts = config_opts

        super().__init__(**kwargs)

        if add_log_args:
            self.register("action", "log_levels", LogLevelAction)
            self.register("action", "log_files", LogFileAction)

            group = self.add_argument_group("Logging options")
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

        if config_opts:
            group = self.add_argument_group("Configuration options")
            file_arg_type = ConfigFileType(config_opts)

            if config_opts.required:
                self.add_argument("config", default=config_opts.default_file,
                                  help="Configuration file (ini file format).",
                                  type=file_arg_type,
                                  nargs="?" if config_opts.default_file
                                            else None)
            else:
                group.add_argument("-c", "--config", dest="config",
                                   metavar="FILENAME",
                                   type=file_arg_type,
                                   default=config_opts.default_file,
                                   help="Configuration file (ini file format).")

            group.add_argument("--config-override", dest="config_overrides",
                               action="append", default=[],
                               metavar="SECTION:OPTION=VALUE",
                               type=config_override,
                               help="Overrides the values for configuration "
                                    "OPTION in [SECTION].")

    def parse_known_args(self, args=None, namespace=None):
        parsed, remaining = super().parse_known_args(args=args,
                                                     namespace=namespace)
        if "config" in parsed and "config_overrides" in parsed:
            config = parsed.config
            for sect, subst in parsed.config_overrides:
                key, val = subst
                if not config.has_section(sect):
                    config.add_section(sect)
                parsed.config.set(sect, key, val)

        if "config" in parsed:
            logging.config.fileConfig(parsed.config)

        return parsed, remaining


class ConfigFileType(argparse.FileType):
    def __init__(self, config_opts):
        super().__init__(mode='r')
        self._opts = config_opts

    def __call__(self, filename):
        try:
            fp = super().__call__(expandvars(expanduser(filename)))
        except Exception as ex:
            if self._opts.default_config:
                fp = StringIO(self._opts.default_config)
            else:
                raise

        config = self._opts.ConfigClass(filename)
        config.readfp(fp)

        return config


def config_override(s):
    """TODO"""
    sect, rhs = s.split(':', 1)
    key, val = rhs.split('=', 1)
    return (sect, (key, val))


    if ':' in opt:
        first, second = opt.split(":")
    else:
        first, second = None, opt
    return first, second
'''

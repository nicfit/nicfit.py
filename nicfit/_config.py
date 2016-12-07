# -*- coding: utf-8 -*-
import os.path
import argparse
import configparser
from io import StringIO
from pathlib import Path
from collections import namedtuple


class Config(configparser.ConfigParser):
    """Class for storing, reading, and writing config."""
    def __init__(self, filename, **kwargs):
        super().__init__(**kwargs)
        self.filename = Path(os.path.expandvars(filename)).expanduser()

    def read(self, filenames=None, encoding=None, touch=False):
        if not self.filename.exists() and touch:
            self.filename.touch()
        with open(str(self.filename), encoding=encoding) as fp:
            self.read_file(fp, source=str(self.filename))
        super().read(filenames or [], encoding=encoding)
        return self

    def write(self, fileobject=None, space_around_delimiters=True):
        if fileobject is None:
            fp = open(str(self.filename), 'w')
        else:
            fp = fileobject

        try:
            super().write(fp, space_around_delimiters=space_around_delimiters)
        finally:
            if fileobject is None:
                fp.close()


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


class ConfigOptions(namedtuple("_ConfigOptions", ["required",
                                                  "default_file",
                                                  "default_config",
                                                  "ConfigClass",
                                                  "override_arg"])):
    def __new__(cls, required=False, default_file=None, default_config=None,
                override_arg=False, ConfigClass=Config):
        return super().__new__(cls, required, default_file, default_config,
                               ConfigClass, override_arg)


def addCommandLineArgs(arg_parser, opts):
    from ._argparse import ArgumentParser

    g = arg_parser.add_argument_group("Configuration options")
    if opts.required:
        arg_parser.add_argument(
            "config", default=opts.default_file,
            help="Configuration file (ini file format).",
            type=ConfigFileType(default_config=opts.default_config),
            nargs="?" if opts.default_file else None)
    else:
        g.add_argument("-c", "--config", dest="config", metavar="FILENAME",
                       type=ConfigFileType(default_config=opts.default_config),
                       default=opts.default_file,
                       help="Configuration file (ini file format).")

    if opts.override_arg:
        if not isinstance(arg_parser, ArgumentParser):
            raise ValueError("nicfit.ArgumentParser type required for "
                             "--config-override support.")

        g.add_argument("--config-override", dest="config_overrides",
                       action="append", metavar="SECTION:OPTION=VALUE",
                       type=_config_override,
                       help="Overrides the value for configuration OPTION in "
                            "[SECTION].")


def _config_override(s):
    sect, rhs = s.split(':', 1)
    key, val = rhs.split('=', 1)
    if not sect or not key:
        raise ValueError("section and key required")
    return (sect, (key, val))

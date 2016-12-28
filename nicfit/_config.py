# -*- coding: utf-8 -*-
import os.path
import argparse
import configparser
from pathlib import Path
from collections import namedtuple


class Config(configparser.ConfigParser):
    """Class for storing, reading, and writing config."""
    def __init__(self, filename, *, config_env_var=None, **kwargs):
        super().__init__(**kwargs)

        if (config_env_var and config_env_var in os.environ and
                Path(os.environ[config_env_var]).exists()):
            with open(os.environ[config_env_var]) as confp:
                self.read_file(confp)

        self.filename = Path(os.path.expanduser(os.path.expandvars(filename))) \
                            if filename else None

    def read(self, filenames=None, encoding=None, touch=False):
        super().read(filenames or [], encoding=encoding)

        if not self.filename.exists() and touch:
            self.filename.touch()

        with open(str(self.filename), encoding=encoding) as fp:
            self.read_file(fp, source=str(self.filename))

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
    """ArgumentParser ``type`` for loading ``Config`` objects."""
    def __init__(self, config_opts=None, encoding="utf-8"):
        super().__init__(mode='r')
        self._encoding = encoding
        self._opts = config_opts or ConfigOpts()

    def __call__(self, filename):
        if not filename and not self._opts.default_config:
            return None

        assert(issubclass(self._opts.ConfigClass, Config))
        config = self._opts.ConfigClass(filename,
                                        config_env_var=self._opts.env_var)

        if self._opts.default_config:
            config.read_string(self._opts.default_config)

        if filename:
            try:
                fp = super().__call__(filename)
                config.readfp(fp)
            except Exception as ex:
                if not self._opts.default_config:
                    raise

        return config


class ConfigOpts(namedtuple("_ConfigOptions", ["required",
                                               "default_file",
                                               "default_config",
                                               "override_arg",
                                               "ConfigClass",
                                               "default_config_opt",
                                               "env_var",
                                              ])):
    # XXX: attrs lib could make this go away
    def __new__(cls, required=False, default_file=None, default_config=None,
                override_arg=False, ConfigClass=Config,
                default_config_opt=None, env_var=None):
        return super().__new__(cls, required, default_file, default_config,
                               override_arg, ConfigClass, default_config_opt,
                               env_var)


def addCommandLineArgs(arg_parser, opts):
    from ._argparse import ArgumentParser

    g = arg_parser.add_argument_group("Configuration options")
    if opts.required:
        arg_parser.add_argument(
            "config", default=opts.default_file,
            help="Configuration file (ini file format).",
            type=ConfigFileType(opts),
            nargs="?" if opts.default_file else None)
    else:
        g.add_argument("-c", "--config", dest="config", metavar="file.ini",
                       type=ConfigFileType(opts),
                       default=ConfigFileType(opts)(opts.default_file),
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

    if opts.default_config_opt:
        if opts.default_config is None:
            raise ValueError("ConfigOpts.default_config_opt requires a value "
                             "in ConfigOpts.default_config")
        g.add_argument(opts.default_config_opt, dest="config_show_default",
                       action="store_true",
                       help="Prints the default configuration.")


def _config_override(s):
    sect, rhs = s.split(':', 1)
    key, val = rhs.split('=', 1)
    if not sect or not key:
        raise ValueError("section and key required")
    return (sect, (key, val))

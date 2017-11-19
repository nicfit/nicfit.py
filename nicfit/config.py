import io
import os.path
import argparse
import configparser
import logging.config
from pathlib import Path
from collections import namedtuple


class Config(configparser.ConfigParser):
    """Class for storing, reading, and writing config."""
    def __init__(self, filename, *, config_env_var=None, touch=False, mode=None,
                 **kwargs):
        super().__init__(**kwargs)

        if (config_env_var and config_env_var in os.environ and
                Path(os.environ[config_env_var]).exists()):
            with open(os.environ[config_env_var]) as confp:
                self.read_file(confp)

        self.filename = Path(os.path.expandvars(str(filename))).expanduser() \
                            if filename else None
        if self.filename:
            if touch:
                if not self.filename.parent.exists():
                    self.filename.parent.mkdir(parents=True)
                if not self.filename.exists():
                    self.filename.touch()
            if mode and self.filename.exists():
                self.filename.chmod(mode)

    def getlist(self, section, option, *, raw=False, vars=None,
                fallback=None):
        """Return the [section] option values as a list.
        The list items must be delimited with commas and/or newlines.
        """
        val = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        values = []
        if val:
            for line in val.split("\n"):
                values += [s.strip() for s in line.split(",")]
        return values

    def setlist(self, section, option, value, *, delim=", "):
        self.set(section, option, delim.join(value))

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

    def __str__(self):
        out = io.StringIO()
        self.write(out)
        out.seek(0)
        return out.read()


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
        if filename:
            filename = os.path.expanduser(os.path.expandvars(filename))

        # Make config, ``filename`` is not yet read.
        config = self._opts.ConfigClass(filename,
                                        config_env_var=self._opts.env_var,
                                        **self._opts.extra_config_opts)
        # Default config? Start with that...
        if self._opts.default_config:
            config.read_string(self._opts.default_config)

        # User file.
        if filename:
            try:
                fp = super().__call__(filename)
                config.read_file(fp)
                if self._opts.init_logging_fileConfig:
                    fp.seek(0)
                    logging.config.fileConfig(fp)
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
                                               "extra_config_opts",
                                               "init_logging_fileConfig",
                                              ])):
    """A namedtuple to describe configuration properties for an application."""
    def __new__(cls, required=False, default_file=None, default_config=None,
                override_arg=False, ConfigClass=Config,
                default_config_opt=None, env_var=None,
                extra_config_opts=None, init_logging_fileConfig=False):
        """
        :param required: A boolean stating whether the config argument is
            required. When ``True`` a positional argument ``config`` is added
            to the command line parser. This argument is required unless
            the ``default_file`` option is set. When ``False`` the arguments
            ``-c/--config`` are added to the argument parser.
        :param default_file: Default config file path.
        :param default_config: A default config string.
        :param override_arg: If True a ``--config-override`` option is added
            to the argument parser to allow command-line over rides of config
            values. See :class:`nicfit._argparse.ArgumentParser`.
        :param ConfigClass: The class type for the configuration object. This
            MUST be either :class:`nicfit._config.Config` or a subclass thereof.
        :param default_config_opt: If not ``None`` it should be a command line
            optional in either short OR long form. When used the the default
            configuration data is printed to stdout.
        :param env_var: When not ``None`` it is the name of an environment
            variable that will be read (if the path exists, not errors when it
            does not) in addition to any other config filenames.
        :param extra_config_opts: A dict of extra keyword arguments to pass to
               the ``ConfigClass`` constructor.
        :param init_logging_fileConfig: If ``True`` the config (default or
               otherwise, is passed to ``logging.config.fileConfig``.
        """
        return super().__new__(cls, required, default_file, default_config,
                               override_arg, ConfigClass, default_config_opt,
                               env_var, extra_config_opts or {},
                               init_logging_fileConfig)


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

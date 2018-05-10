import io
import os
import attr
import argparse
import configparser
import logging.config
from pathlib import Path


class Config(configparser.ConfigParser):
    """Class for storing, reading, and writing config."""
    def __init__(self, filename, *, config_env_var=None, touch=False, mode=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.input_filenames = []

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
            elif not self.filename.exists():
                raise FileNotFoundError(self.filename)

            if (self.filename.exists() and mode and
                    self.filename.stat().st_mode & 0o777 != mode):
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
        self.set(section, option, delim.join([str(v) for v in value]))

    # XXX: no override for read_string, read_string -> read_file

    def read_file(self, f, source="<file>"):
        self.input_filenames.append(source)
        return super().read_file(f, source=source)

    def read_dict(self, dictionary, source='<dict>'):
        self.input_filenames.append(source)
        return super().read_dict(dictionary, source=source)

    def read(self, filenames=None, encoding=None):
        filenames = filenames or []

        super().read(filenames, encoding=encoding)
        self.input_filenames += filenames

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
        self._opts = config_opts or ConfigOpts()
        self._encoding = encoding

    def __call__(self, filename):
        if not filename and not self._opts.default_config:
            return None

        assert(issubclass(self._opts.ConfigClass, Config))
        if filename:
            filename = os.path.expanduser(os.path.expandvars(filename))

        config = self._opts.ConfigClass(filename,
                                        **self._opts.configClassOpts(),
                                        **self._opts.configparser_opts)

        # Default config? Start with that...
        if self._opts.default_config:
            config.read_string(self._opts.default_config, source="<default>")

        # User file.
        if filename:
            config.read()
            if self._opts.init_logging_fileConfig:
                logging.config.fileConfig(config)

        return config


@attr.s(frozen=True)
class ConfigOpts:
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
    :param config_env_var: When not ``None`` it is the name of an env
        variable that will be read (if the path exists, not errors when it
        does not) in addition to any other config filenames.
    :param config_parsers_opts: A dict of extra
        ``configparser.ConfigParser`` keyword arguments to pass to the
         ``ConfigClass`` constructor.
    :param init_logging_fileConfig: If ``True`` the config (default or
           otherwise, is passed to ``logging.config.fileConfig``.
    """
    required = attr.ib(default=False)
    default_file = attr.ib(default=None)
    default_config = attr.ib(default=None)
    override_arg = attr.ib(default=False)
    ConfigClass = attr.ib(default=Config)
    default_config_opt = attr.ib(default=None)
    config_env_var = attr.ib(default=None)
    init_logging_fileConfig = attr.ib(default=False)
    configparser_opts = attr.ib(default=attr.Factory(dict))
    touch = attr.ib(default=False)
    mode = attr.ib(default=None)

    def configClassOpts(self):
        return dict(touch=self.touch,
                    mode=self.mode)


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

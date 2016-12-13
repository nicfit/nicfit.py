# -*- coding: utf-8 -*-
import argparse


class ArgumentParser(argparse.ArgumentParser):
    """ArgumentParser with optional logging options."""

    def __init__(self, add_log_args=False, config_opts=None, **kwargs):
        super().__init__(**kwargs)
        if add_log_args:
            from . import _logging
            _logging.addCommandLineArgs(self)
        if config_opts:
            from . import _config
            _config.addCommandLineArgs(self, config_opts)
        self._config_opts = config_opts

    def parse_known_args(self, args=None, namespace=None):
        parsed, remaining = super().parse_known_args(args=args,
                                                     namespace=namespace)

        if "config" in parsed and "config_overrides" in parsed:
            config = parsed.config
            overrides = parsed.config_overrides or []
            for sect, subst in overrides:
                key, val = subst
                if not config.has_section(sect):
                    config.add_section(sect)
                config.set(sect, key, val)

        if "config_show_default" in parsed and parsed.config_show_default:
            self.exit(0, self._config_opts.default_config)
            # does not return

        return parsed, remaining

    def add_subparsers(self, add_help_subcmd=False, **kwargs):
        subparser = super().add_subparsers(**kwargs)
        if add_help_subcmd:
            # 'help' subcommand; turns it into the less intuitive --help format.
            # e.g.  cmd help subcmd  ==> cmd subcmd --help
            def _help(args, config):
                if args.command:
                    self.parse_args([args.command, "--help"])
                else:
                    self.print_help()
                self.exit(0)

            help = subparser.add_parser("help",
                                        help="Show help for a sub command")
            help.set_defaults(func=_help)
            help.add_argument("command", nargs='?', default=None)

        return subparser

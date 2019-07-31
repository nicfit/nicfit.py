import sys
import argparse
import gettext
_ = gettext.gettext


class ArgumentParser(argparse.ArgumentParser):
    """ArgumentParser with optional logging, config, and sub-command support."""

    def __init__(self, add_log_args=False, config_opts=None, **kwargs):
        super().__init__(**kwargs)

        if add_log_args:
            from . import logger
            logger.addCommandLineArgs(self)
        self._add_log_args = add_log_args

        if config_opts:
            from . import config
            config.addCommandLineArgs(self, config_opts)
        self._config_opts = config_opts
        # For python <= 3.6, where subcmds are optional
        self._subcmd_required = None

    def parse_known_args(self, args=None, namespace=None):
        from . import logger

        parsed, remaining = super().parse_known_args(args=args,
                                                     namespace=namespace)

        # Required sub command support for Python < 3.7
        if self._subcmd_required is not None:
            req, dest = self._subcmd_required
            if req and dest and (not hasattr(parsed, dest) or
                                 not getattr(parsed, dest)):
                self.error(_('the following arguments are required: %s') % dest)

        if "config" in parsed and "config_overrides" in parsed:
            config = parsed.config
            overrides = parsed.config_overrides or []
            for sect, subst in overrides:
                key, val = subst
                if not config.has_section(sect):
                    config.add_section(sect)
                config.set(sect, key, val)

        if "config_show_default" in parsed and parsed.config_show_default:
            # Not using the msg facility of self.exit because it goes to stderr
            print(self._config_opts.default_config)
            self.exit(0)
            # does not return

        if self._add_log_args:
            parsed.applyLoggingOpts = logger.applyLoggingOpts

        return parsed, remaining

    def add_subparsers(self, add_help_subcmd=False, required=True,
                       dest="subcmd", **kwargs):
        if "parser_class" not in kwargs:
            kwargs["parser_class"] = ArgumentParser

        if sys.version_info[:2] >= (3, 7):
            subparser = super().add_subparsers(required=required, dest=dest,
                                               **kwargs)
        else:
            self._subcmd_required = (
                required, dest,
            )
            subparser = super().add_subparsers(dest=dest, **kwargs)

        if add_help_subcmd:
            # 'help' subcommand; turns it into the less intuitive --help format.
            # e.g.  cmd help subcmd  ==> cmd subcmd --help
            def _help(args):
                if args.command:
                    self.parse_args([args.command, "--help"])
                else:
                    self.print_help()
                self.exit(0)

            help = subparser.add_parser("help",
                                        help="Show help for a sub command")
            help.set_defaults(command_func=_help)
            help.add_argument("command", nargs='?', default=None)

        return subparser

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

        return parsed, remaining

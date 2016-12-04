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
            _config.addCommandLineArgs(self, **config_opts)

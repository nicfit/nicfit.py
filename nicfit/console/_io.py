# -*- coding: utf-8 -*-
from sys import stdout, stderr


def pout(msg, log=None):
    """Print 'msg' to stdout, and option 'log' at info level."""
    _print(msg, stdout, log_func=log.info if log else None)


def perr(msg, log=None):
    """Print 'msg' to stderr, and option 'log' at info level."""
    _print(msg, stderr, log_func=log.error if log else None)


def _print(msg, file, log_func=None):
    print(msg, file=file)
    if log_func:
        log_func(msg)

# -*- coding: utf-8 -*-
from collections import namedtuple

from ._argparse import ArgumentParser
from ._logging import rootLogger, getLogger, DEFAULT_LOGGING_CONFIG

from .app import Application


__project_name__ = 'nicfit.py'
__project_slug__ = 'nicfit.py'
__author__ = 'Travis Shirk'
__author_email__ = 'travis@pobox.com'
__url__ = 'https://github.com/nicfit/nicfit.py'
__description__ = 'Common Python utils by Travis Shirk'

__version__ = '0.1.0'
__release__ = __version__.split('-')[1] if '-' in __version__ else "final"
__version_info__   = \
    namedtuple("Version", "major, minor, maint, release")(
        *(tuple((int(v) for v in __version__.split('-')[0].split('.'))) +
          tuple((__release__,))))

__years__ = "2016"
__license__ = 'GPL'

__version_txt__ = """
%(__name__)s %(__version__)s (C) Copyright %(__years__)s %(__author__)s
This program comes with ABSOLUTELY NO WARRANTY! See LICENSE for details.
Run with --help/-h for usage information or read the docs at
%(__url__)s
""" % (locals())


# -*- coding: utf-8 -*-
from collections import namedtuple

from ._argparse import ArgumentParser                                     # noqa
from ._config import Config, ConfigOpts                                   # noqa
from ._logging import getLogger, LOGGING_CONFIG                           # noqa
from .app import Application                                              # noqa

log = getLogger(__package__)
__version__ = '0.2.0-beta4'
__release_name__ = ""
__release__ = __version__.split('-')[1] if '-' in __version__ else "final"

__project_name__ = 'nicfit.py'
__project_slug__ = 'nicfit.py'
__author__ = 'Travis Shirk'
__author_email__ = 'travis@pobox.com'
__url__ = 'https://github.com/nicfit/nicfit.py'
__description__ = 'Common Python utils (App, logging, config, etc.)'

__version_info__ = \
    namedtuple("Version", "major, minor, maint, release")(
        *(tuple((int(v) for v in __version__.split('-')[0].split('.'))) +
          tuple((__release__,))))

__years__ = "2016"
__license__ = 'MIT'

__version_txt__ = """
%(__name__)s %(__version__)s (C) Copyright %(__years__)s %(__author__)s
This program comes with ABSOLUTELY NO WARRANTY! See LICENSE for details.
Run with --help/-h for usage information or read the docs at
%(__url__)s
""" % (locals())

log = getLogger(__package__)

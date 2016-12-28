# -*- coding: utf-8 -*-
from collections import namedtuple

__version__ = '0.4.0'
__release_name__ = ""
__release__ = __version__.split('-')[1] if '-' in __version__ else "final"

__project_name__ = 'nicfit.py'
__project_slug__ = 'nicfit.py'
__author__ = 'Travis Shirk'
__author_email__ = 'travis@pobox.com'
__url__ = 'https://github.com/nicfit/nicfit.py'
__description__ = 'Common Python utils (App, logging, config, etc.) [Python3.4]'

__version_info__ = \
    namedtuple("Version", "major, minor, maint, release")(
        *(tuple((int(v) for v in __version__.split('-')[0].split('.'))) +
          tuple((__release__,))))

__years__ = "2016-2017"
__license__ = 'MIT'

__version_txt__ = """
%(__name__)s %(__version__)s (C) Copyright %(__years__)s %(__author__)s
This program comes with ABSOLUTELY NO WARRANTY! See LICENSE for details.
Run with --help/-h for usage information or read the docs at
%(__url__)s
""" % (locals())

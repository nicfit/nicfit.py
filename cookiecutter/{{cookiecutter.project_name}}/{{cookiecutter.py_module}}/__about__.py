# -*- coding: utf-8 -*-
from collections import namedtuple

__version__ = "{{ cookiecutter.version }}"
__release_name__ = ""
__years__ = "{{ cookiecutter.year }}"

__project_name__ = "{{ cookiecutter.project_name }}"
__project_slug__ = "{{ cookiecutter.project_slug }}"
__author__ = "{{ cookiecutter.full_name }}"
__author_email__ = "{{ cookiecutter.email }}"
__url__ = "{{ cookiecutter.web }}"
__description__ = "{{ cookiecutter.project_short_description }}"
__long_description__ = "{{ cookiecutter.project_long_description }}"
__license__ = "{{ cookiecutter.license }}"

__release__ = __version__.split("-")[1] if "-" in __version__ else "final"
__version_info__ = \
    namedtuple("Version", "major, minor, maint, release")(
        *(tuple((int(v) for v in __version__.split("-")[0].split("."))) +
          tuple((__release__,))))


__version_txt__ = """
%(__name__)s %(__version__)s (C) Copyright %(__years__)s %(__author__)s
This program comes with ABSOLUTELY NO WARRANTY! See LICENSE for details.
Run with --help/-h for usage information or read the docs at
%(__url__)s
""" % (locals())

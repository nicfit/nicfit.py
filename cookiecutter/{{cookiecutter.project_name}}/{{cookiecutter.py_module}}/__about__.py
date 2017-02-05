# -*- coding: utf-8 -*-
from collections import namedtuple

__version__ = "{{ cookiecutter.version }}"
__release_name__ = ""
__years__ = "{{ cookiecutter.year }}"

__project_name__ = "{{ cookiecutter.project_name }}"
__project_slug__ = "{{ cookiecutter.project_slug }}"
__pypi_name__ = "{{ cookiecutter.pypi_repo_name }}"
__author__ = "{{ cookiecutter.full_name }}"
__author_email__ = "{{ cookiecutter.email }}"
__url__ = "{{ cookiecutter.web }}"
__description__ = "{{ cookiecutter.project_short_description }}"
__long_description__ = "{{ cookiecutter.project_long_description }}"
__license__ = "{{ cookiecutter.license }}"
{%- if cookiecutter.use_github == "yes" %}
__github_url__ = "https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}",
{%- else %}
__bitbucket_url__ = "https://bitbucket.org/{{ cookiecutter.bitbucket_username }}/{{ cookiecutter.project_slug }}",
{%- endif %}

__release__ = __version__.split("-")[1] if "-" in __version__ else "final"
_v = tuple((int(v) for v in __version__.split("-")[0].split(".")))
__version_info__ = \
    namedtuple("Version", "major, minor, maint, release")(
        *(_v + (tuple((0,)) * (3 - len(_v))) +
          tuple((__release__,))))
del _v
__version_txt__ = """
%(__name__)s %(__version__)s (C) Copyright %(__years__)s %(__author__)s
This program comes with ABSOLUTELY NO WARRANTY! See LICENSE for details.
Run with --help/-h for usage information or read the docs at
%(__url__)s
""" % (locals())

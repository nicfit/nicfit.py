===============================
{{ cookiecutter.project_name }}
===============================

{{ cookiecutter.project_short_description}}

Status
------

+---------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *PyPi*                                | .. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg                                                                                 |
|                                       |    :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}/                                                                                    |
|                                       |    :alt: Latest Version                                                                                                                                      |
|                                       | .. image:: https://img.shields.io/pypi/l/{{ cookiecutter.project_slug }}.svg                                                                                 |
|                                       |    :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}/                                                                                    |
|                                       |    :alt: License                                                                                                                                             |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *Python versions and implementations* | .. image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_slug }}.svg                                                                        |
|                                       |    :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}/                                                                                    |
|                                       |    :alt: Supported Python versions                                                                                                                           |
|                                       | .. image:: https://img.shields.io/pypi/implementation/{{ cookiecutter.project_slug }}.svg                                                                    |
|                                       |    :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}/                                                                                    |
|                                       |    :alt: Supported Python implementations                                                                                                                    |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
{%- if cookiecutter.use_travis_ci == "yes" -%}
| *Builds and tests coverage*           | .. image:: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg?branch=master                                        |
|                                       |    :target: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}                                                         |
|                                       |    :alt: Build Status                                                                                                                                        |
|                                       | .. image:: https://coveralls.io/repos/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/badge.svg                                           |
|                                       |    :target: https://coveralls.io/r/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}                                                        |
|                                       |    :alt: Coverage Status                                                                                                                                     |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
{%- endif -%}
{%- if cookiecutter.use_github == "yes" -%}
| *Github*                              | .. image:: https://img.shields.io/github/downloads/atom/atom/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg?style=social&label=Watch |
|                                       |    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}                                                            |
|                                       |    :alt: Github watchers                                                                                                                                     |
|                                       | .. image:: https://img.shields.io/github/stars/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg?style=social&label=Star                |
|                                       |    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}                                                            |
|                                       |    :alt: Github stargazers                                                                                                                                   |
|                                       | .. image:: https://img.shields.io/github/forks/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg?style=social&label=Fork                |
|                                       |    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}                                                            |
|                                       |    :alt: Github forks                                                                                                                                        |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
{%- endif -%}

* Free software: {{ cookiecutter.license }} license
* Documentation: https://{{ cookiecutter.project_slug }}.readthedocs.org.

Features
--------

* TODO

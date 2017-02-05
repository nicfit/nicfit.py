===============================
{{ cookiecutter.project_name }}
===============================

{{ cookiecutter.project_short_description}}

Status
------
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.pypi_repo_name }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.pypi_repo_name }}/
   :alt: Latest Version
.. image:: https://img.shields.io/pypi/status/{{ cookiecutter.pypi_repo_name }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.pypi_repo_name }}/
   :alt: Project Status
.. image:: https://travis-ci.org/nicfit/{{ cookiecutter.github_repo }}.svg?branch=master
   :target: https://travis-ci.org/nicfit/{{ cookiecutter.github_repo }}
   :alt: Build Status
.. image:: https://img.shields.io/pypi/l/{{ cookiecutter.pypi_repo_name }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.pypi_repo_name }}/
   :alt: License
.. image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.pypi_repo_name }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.pypi_repo_name }}/
   :alt: Supported Python versions
.. image:: https://coveralls.io/repos/nicfit/{{ cookiecutter.github_repo }}/badge.svg
   :target: https://coveralls.io/r/nicfit/{{ cookiecutter.github_repo }}
   :alt: Coverage Status

{%- if cookiecutter.use_rtd == "yes" %}
* Documentation: https://{{ cookiecutter.project_slug }}.readthedocs.org.
{%- endif %}

Features
--------

* Free software: {{ cookiecutter.license }} license

===============================
{{ cookiecutter.project_name }}
===============================

{{ cookiecutter.project_short_description}}

Status
------
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}/
   :alt: Latest Version
.. image:: https://img.shields.io/pypi/status/{{ cookiecutter.project_slug }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}/
   :alt: Project Status
.. image:: https://travis-ci.org/nicfit/{{ cookiecutter.project_slug }}.svg?branch=master
   :target: https://travis-ci.org/nicfit/{{ cookiecutter.project_slug }}
   :alt: Build Status
.. image:: https://img.shields.io/pypi/l/{{ cookiecutter.project_slug }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}/
   :alt: License
.. image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_slug }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}/
   :alt: Supported Python versions
.. image:: https://coveralls.io/repos/nicfit/{{ cookiecutter.project_slug }}/badge.svg
   :target: https://coveralls.io/r/nicfit/{{ cookiecutter.project_slug }}
   :alt: Coverage Status

{%- if cookiecutter.use_rtd == "yes" %}
* Documentation: https://{{ cookiecutter.project_slug }}.readthedocs.org.
{%- endif %}

Features
--------

* Free software: {{ cookiecutter.license }} license

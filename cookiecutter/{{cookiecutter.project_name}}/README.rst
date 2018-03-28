===============================
{{ cookiecutter.project_name }} README
===============================

|Build Status| |License| |PyPI| |Python versions| |Coverage| |Status|

{{ cookiecutter.project_short_description}}

{%- if cookiecutter.use_rtd == "yes" %}
* Documentation: https://{{ cookiecutter.project_slug }}.readthedocs.org.
{%- endif %}

Features
--------
* Free software: {{ cookiecutter.license }} license


.. |Build Status| image:: https://travis-ci.org/nicfit/{{ cookiecutter.github_repo }}.svg?branch=master
   :target: https://travis-ci.org/nicfit/{{ cookiecutter.github_repo }}
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/{{ cookiecutter.pypi_repo_name }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.pypi_repo_name }}/
   :alt: Latest Version
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.pypi_repo_name }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.pypi_repo_name }}/
   :alt: Supported Python versions
.. |License| image:: https://img.shields.io/pypi/l/{{ cookiecutter.pypi_repo_name }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.pypi_repo_name }}/
   :alt: License
.. |Status| image:: https://img.shields.io/pypi/status/{{ cookiecutter.pypi_repo_name }}.svg
   :target: https://pypi.python.org/pypi/{{ cookiecutter.pypi_repo_name }}/
   :alt: Project Status
.. |Coverage| image:: https://coveralls.io/repos/nicfit/{{ cookiecutter.github_repo }}/badge.svg
   :target: https://coveralls.io/r/nicfit/{{ cookiecutter.github_repo }}
   :alt: Coverage Status

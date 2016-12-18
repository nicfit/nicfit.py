#!/usr/bin/env python
import os
import shutil
import datetime
from pathlib import Path

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(str(Path(PROJECT_DIRECTORY) / filepath))


def replace_contents(filename, what, replacement):
    with filename.open() as fh:
        changelog = fh.read()
    with filename.open('w') as fh:
        fh.write(changelog.replace(what, replacement))


if __name__ == "__main__":
    today = datetime.date.today()

    for path in [Path("HISTORY.rst"),
                 Path('{{ cookiecutter.py_module }}') / "__init__.py",
                 Path('docs') / 'conf.py']:

        replace_contents(path, '<TODAY>', today.strftime("%Y-%m-%d"))
        replace_contents(path, '<YEAR>', today.strftime("%Y"))

    if '{{ cookiecutter.use_pypi_deployment_with_travis }}' == 'no':
        remove_file('travis_pypi_setup.py')

    if '{{ cookiecutter.use_paver }}' == 'no':
        remove_file('pavement.py')
    if '{{ cookiecutter.use_make }}' == 'no':
        remove_file('Makefile')

    if '{{ cookiecutter.use_bitbucket }}' == 'no':
        remove_file('.hgignore')
    if '{{ cookiecutter.use_github }}' == 'no':
        remove_file('.gitignore')

    if ('{{ cookiecutter.support_python2 }}',
        '{{ cookiecutter.support_python2 }}') != ("yes", "yes"):
        remove_file("{{ cookiecutter.py_module }}/_compat.py")

    for f in Path("licenses").iterdir():
        f.unlink()
    Path("licenses").rmdir()

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


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if (not os.path.exists(d) or
                    os.stat(s).st_mtime - os.stat(d).st_mtime > 1):
                shutil.copy2(s, d)


if __name__ == "__main__":
    today = datetime.date.today()

    for path in [Path("HISTORY.rst"),
                 Path('{{ cookiecutter.py_module }}') / "__init__.py",
                 Path('docs') / 'conf.py']:

        replace_contents(path, '<TODAY>', today.strftime("%Y-%m-%d"))
        replace_contents(path, '<YEAR>', today.strftime("%Y"))

    if '{{ cookiecutter.use_travis_ci }}' == 'no':
        remove_file('.travis.yml')
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

    for f in Path("licenses").iterdir():
        f.unlink()
    Path("licenses").rmdir()

    if "{{ cookiecutter.src_dir }}" != ".":
        src_d = Path("{{ cookiecutter.src_dir}}")
        if not src_d.exists():
            src_d.mkdir(parents=True)
        copytree("{{ cookiecutter.py_module }}",
                 str(src_d / "{{ cookiecutter.py_module }}"))
        copytree("tests", str(src_d / "tests"))
        shutil.rmtree("{{ cookiecutter.py_module }}")
        shutil.rmtree("tests")

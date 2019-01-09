#!/usr/bin/env python
import os
import shutil
import datetime
from pathlib import Path

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    f = Path(PROJECT_DIRECTORY) / filepath
    if f.is_dir():
        shutil.rmtree(str(f))
    else:
        f.unlink()


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

    if '{{ cookiecutter.use_github }}' == 'yes':
        remove_file('.hgignore')
        if not Path(".git").exists():
            os.system("git init .")
        shutil.move("git-commit-msg", ".git/hooks/commit-msg")
    else:
        remove_file('.gitignore')
        remove_file('git-commit-msg')

    for path in [Path("HISTORY.rst"),
                 Path('{{ cookiecutter.py_module }}') / "__about__.py",
                 Path('docs') / 'conf.py',
                ]:
        replace_contents(path, '<TODAY>', today.strftime("%Y-%m-%d"))
        replace_contents(path, '<YEAR>', today.strftime("%Y"))

    tox_envlist = []
    for py, on in [("py26", "{{ cookiecutter.py26 }}"),
                   ("py27", "{{ cookiecutter.py27 }}"),
                   ("py33", "{{ cookiecutter.py33 }}"),
                   ("py34", "{{ cookiecutter.py34 }}"),
                   ("py35", "{{ cookiecutter.py35 }}"),
                   ("py36", "{{ cookiecutter.py36 }}"),
                   ("py37", "{{ cookiecutter.py37 }}"),
                   ("pypy", "{{ cookiecutter.pypy }}"),
                   ("pypy3", "{{ cookiecutter.pypy3 }}"),
                  ]:
        if on == "yes":
            tox_envlist.append(py)
    replace_contents(Path("tox.ini"), '@TOX_ENVLIST@',
                     ", ".join(tox_envlist))

    if '{{ cookiecutter.use_travis_ci }}' == 'no':
        remove_file('.travis.yml')
    if '{{ cookiecutter.use_pypi_deployment_with_travis }}' == 'no':
        remove_file('travis_pypi_setup.py')

    if '{{ cookiecutter.use_paver }}' == 'no':
        remove_file('pavement.py')
    if '{{ cookiecutter.use_make }}' == 'no':
        remove_file('Makefile')

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

    domain = "{{ cookiecutter.gettext_domain }}"
    if domain == "None":
        shutil.rmtree("locale")
    else:
        gk = Path("locale/.gitkeep")
        if gk.exists():
            gk.unlink()

    if '{{ cookiecutter.add_docs }}' == 'no':
        remove_file('docs')

    if '{{ cookiecutter.requirements_yaml }}' == 'no':
        remove_file('requirements')

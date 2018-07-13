#!/usr/bin/env python
import io
import os
import re
import sys
import shlex
import typing
import logging
import setuptools
import subprocess
import configparser
from pathlib import Path
from operator import attrgetter
from setuptools.command.test import test as _TestCommand
from setuptools.command.develop import develop as _DevelopCommand
from setuptools.command.install import install as _InstallCommand

__version__ = "1.0a0"
__project_name__ = "Parcyl"
__url__ = "https://github.com/nicfit/parcyl"
__author__ = "Travis Shirk"
__author_email__ = "travis@pobox.com"

_EXTRA = "extra_"
_REQ_D = Path("requirements")
_SETUP_CFG = Path("setup.cfg")
_CFG_SECT = f"tool:{__project_name__.lower()}"
_log = logging.getLogger(__project_name__.lower())

find_packages = setuptools.find_packages


def setup(**setup_attrs):
    """A shortcut help function to use when you don't need the  `Setup` object.
    >>> import parcyl
    >>> setup =  parcyl.setup(...)
    instead of
    >>> import parcyl
    >>> setup =  parcyl.Setup(...)
    >>> setup()
    """
    s = Setup(**setup_attrs)
    s()
    return s


class Setup:
    """
    TODO
    """
    def __init__(self, **setup_attrs):
        """TODO
        :param setup_attrs:
        """
        # Install commands (TODO: merge with any existing commands)
        setup_attrs["cmdclass"] = {"install": InstallCommand,
                                   "test": TestCommand,
                                   "pytest": PyTestCommand,
                                   "develop": DevelopCommand,
                                  }

        # Requirements
        self.requirements = None
        if _SETUP_CFG.exists():
            self.requirements = Requirements()
            for setup_arg, attr in [("install_requires", attrgetter("install")),
                                    ("tests_require", attrgetter("test")),
                                    ("extras_require", attrgetter("extras")),
                                    ("setup_requires", attrgetter("setup")),
                                   ]:
                if setup_arg not in setup_attrs:
                    setup_attrs[setup_arg] = attr(self.requirements)
                else:
                    raise ValueError(
                        f"`{setup_arg}` must be set via requirements file.")

        # Final args
        self._setup_attrs = dict(setup_attrs)

    def __call__(self, **setup_attrs):
        attrs = dict(self._setup_attrs)
        attrs.update(setup_attrs)
        setuptools.setup(**attrs)

    def with_packages(self, *pkg_dirs, exclude=None):
        """TODO
        :param pkg_dirs:
        :param exclude:
        :return:
        """
        pkgs = []
        if "pacakges" not in self._setup_attrs:
            self._setup_attrs["packages"] = []
        for d in pkg_dirs:
            pkgs += find_packages(d, exclude=exclude)
        self._setup_attrs["packages"] += pkgs
        return self


class Requirements:
    """
    TODO
    """
    _SECTS = ("install", "test", "dev", "setup")

    def __init__(self):
        self._req_format = None
        self._req_dict = self._loadIni(_SETUP_CFG)

    def _getter(self, sect):
        return self._req_dict[sect] if sect in self._req_dict else []

    @property
    def install(self):
        return self._getter("install")

    @property
    def test(self):
        return self._getter("test")

    @property
    def dev(self):
        return self._getter("dev")

    @property
    def setup(self):
        return self._getter("setup")

    @property
    def extras(self):
        extras = {}
        for sect in [s for s in self._req_dict if s.startswith(_EXTRA)]:
            extras[sect[len(_EXTRA):]] = self._req_dict[sect]
        return extras

    def _loadIni(self, req_ini):
        reqs = {}
        req_config = configparser.ConfigParser()
        req_config.read(req_ini)

        for opt in req_config.options(_CFG_SECT):
            if opt in self._SECTS or opt.startswith(_EXTRA):
                reqs[opt] = list()
                deps = req_config.get(_CFG_SECT, opt)
                if deps:
                    for line in deps.split("\n"):
                        reqs[opt] += [s.strip() for s in line.split(",")]

        return reqs

    def write(self, include_extras=False):
        """TODO
        :param include_extras:
        :return:
        """
        def _writeReqsFile(filepath, reqs):
            def _splitPkg(line):
                pkg, ver = line, None
                for c in ("=", ">", "<"):
                    i = line.find(c)
                    if i != -1:
                        pkg = line[0:i]
                        ver = line[i:]
                        break
                return pkg, ver

            def _readReq(file):
                reqs = {}
                file.seek(0)
                for line in [l.strip() for l in file.readlines()
                             if l.strip() and not l.startswith("#")]:
                    pkg, version = _splitPkg(line)
                    reqs[pkg] = version
                return reqs

            file_exists = filepath.exists()
            with filepath.open("r+" if file_exists else "w") as fp:
                new = {}
                curr = _readReq(fp) if file_exists else {}

                for r in [r.strip() for r in reqs if r and r.strip()]:
                    pkg, ver = _splitPkg(r)
                    if ver is None and pkg in curr:
                        ver = curr[pkg]
                    new[pkg] = ver

                fp.seek(0)
                fp.truncate(0)
                for pkg in sorted(new.keys()):
                    ver = new[pkg] or ""
                    fp.write("{pkg}{ver}\n".format(**locals()))
                print(f"Wrote {filepath}")

        if not _REQ_D.exists():
            raise NotADirectoryError(str(_REQ_D))

        for req_grp in [
                k for k in self._req_dict.keys() if self._req_dict[k]
        ]:
            _writeReqsFile(_REQ_D / f"{req_grp}.txt", self._req_dict[req_grp])

        # Make top-level requirements.txt files
        pkg_reqs = []
        for name, pkgs in self._req_dict.items():
            if name == "install" or (name.startswith(_EXTRA) and
                                     include_extras):
                pkg_reqs += pkgs or []
        if pkg_reqs:
            _writeReqsFile(Path("requirements.txt"), pkg_reqs)


about_file_attrs_map = {"name": "__project_name__",
                        "version": "__version__",
                        "author": "__author__",
                        "author_email": "__author_email__",
                        "url": "__url__",
                        "license": "__license__",
                        "description": "__description__",
                        "release_name": "__release_name__",
                        "github_url": "__github_url__",
                       }


def setupAttrFromInfoFile(info_filename: typing.Union[Path, str],
                          attr_map: dict=None, quiet=False):
    """TODO
    :param info_filename:
    :param attr_map:
    :param quiet:
    :return:
    """
    info_dict = {}
    if not isinstance(info_filename, Path):
        info_filename = Path(info_filename)
    attr_map = attr_map or about_file_attrs_map

    # TODO: load .py files and use the values directly. Fixes the multiline prob
    # TODO: ^^^ but can't do imports for things than may not be installed yet.
    with io.open(str(info_filename), encoding='utf-8') as infof:
        for line in infof:
            for what in attr_map.keys():
                rex = re.compile(rf"{attr_map[what]}\s*=\s*['\"](.*?)['\"]")
                m = rex.match(line.strip())
                if not m:
                    continue
                info_dict[what] = m.groups()[0]

    vparts = info_dict["version"].split("-", maxsplit=1)
    info_dict["release"] = vparts[1] if len(vparts) > 1 else "final"

    if not quiet:
        for what in attr_map:
            if what not in info_dict:
                print(f"Package info not found: {what}")

    return info_dict


def _pipInstall(*pkgs):
    if len(pkgs):
        pkgs = list([shlex.quote(p) for p in pkgs])
        os.system(f"pip install {' '.join(pkgs)}")


def _pipCompile(req_file: Path):
    subprocess.run(f"pip-compile {req_file}", shell=True, check=True)


class InstallCommand(_InstallCommand):
    def run(self):
        _pipInstall(*self.distribution.install_requires)
        return super().run()


class DevelopCommand(_DevelopCommand):
    def run(self):
        _pipInstall(*self.distribution.install_requires)
        _pipInstall(*self.distribution.tests_require)
        _pipInstall(*Requirements().dev)

        for ex in self.distribution.extras_require:
            _pipInstall(*self.distribution.extras_require[ex])

        return super().run()


class TestCommand(_TestCommand):
    def run(self):
        _pipInstall(*self.distribution.tests_require)
        _pipInstall(*self.distribution.install_requires)
        for ex in self.distribution.extras_require:
            _pipInstall(*self.distribution.extras_require[ex])

        return super().run()


class PyTestCommand(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        _TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


def _main():
    import argparse

    p = argparse.ArgumentParser(description="Python project packaging helper.")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--install", action="store_true")
    p.add_argument("--requirements", action="store_true")
    p.add_argument("--freeze", action="store_true")
    args = p.parse_args()

    if args.install:
        parcyl_py = Path(f"{__project_name__.lower()}.py")
        if parcyl_py.exists():
            print(f"{parcyl_py} already exists, remove and try again",
                  file=sys.stderr)
            return 1
        print(f"Writing {parcyl_py}")
        parcyl_py.write_bytes(Path(__file__).read_bytes())
        parcyl_py.chmod(0o755)

    if args.requirements:
        req = Requirements()
        req.write()

    if args.freeze:
        reqs_txt = Path("requirements.txt")
        req_files = [reqs_txt] if reqs_txt.exists() else []
        req_files += list(_REQ_D.glob("*.txt")) if _REQ_D.exists() else []

        for f in req_files:
            try:
                if f.exists():
                    print(f"Compiling {f}...")
                    _pipCompile(f)
            except subprocess.CalledProcessError as err:
                print(err, file=sys.stderr)
                return err.returncode


if __name__ == "__main__":
    sys.exit(_main() or 0)

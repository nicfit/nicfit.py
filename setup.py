#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import warnings
from setuptools import setup, find_packages
from setuptools.command.install import install

classifiers = [
    "Intended Audience :: Developers",
    "Operating System :: POSIX",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
]


def getPackageInfo():
    info_dict = {}
    info_keys = ["version", "name", "author", "author_email", "url", "license",
                 "description", "release_name", "github_url"]
    key_remap = {"name": "pypi_name"}

    # __about__
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           ".",
                           "nicfit",
                           "__about__.py")) as infof:
        for line in infof:
            for what in info_keys:
                rex = re.compile(r"__{what}__\s*=\s*['\"](.*?)['\"]"
                                 .format(what=what if what not in key_remap
                                                   else key_remap[what]))

                m = rex.match(line.strip())
                if not m:
                    continue
                info_dict[what] = m.groups()[0]

    if sys.version_info[:2] >= (3, 4):
        vparts = info_dict["version"].split("-", maxsplit=1)
    else:
        vparts = info_dict["version"].split("-", 1)
    info_dict["release"] = vparts[1] if len(vparts) > 1 else "final"

    # Requirements
    requirements, extras = requirements_yaml()
    info_dict["install_requires"] = requirements["main"] \
                                        if "main" in requirements else []
    info_dict["tests_require"] = requirements["test"] \
                                     if "test" in requirements else []
    info_dict["extras_require"] = extras

    # Info
    readme = ""
    if os.path.exists("README.rst"):
        with open("README.rst") as readme_file:
            readme = readme_file.read()
    history = ""
    if os.path.exists("HISTORY.rst"):
        with open("HISTORY.rst") as history_file:
            history = history_file.read().replace(".. :changelog:", "")
    info_dict["long_description"] = readme + "\n\n" + history

    return info_dict, requirements


def requirements_yaml():
    EXTRA = "extra_"
    reqs = {}
    reqfile = os.path.join("requirements", "requirements.yml")
    if os.path.exists(reqfile):
        with open(reqfile) as fp:
            curr = None
            for line in [l for l in fp.readlines() if l.strip()]:
                if curr is None or line.lstrip()[0] != "-":
                    curr = line.split(":")[0]
                    reqs[curr] = []
                else:
                    line = line.strip()
                    assert line[0] == "-"
                    r = line[1:].strip()
                    if r:
                        reqs[curr].append(r)

    return (reqs, {x[len(EXTRA):]: vals
                     for x, vals in reqs.items() if x.startswith(EXTRA)})


class PipInstallCommand(install, object):
    def run(self):
        reqs = " ".join(["'%s'" % r for r in PKG_INFO["install_requires"]])
        os.system("pip install " + reqs)
        # XXX: py27 compatible
        return super(PipInstallCommand, self).run()


PKG_INFO, REQUIREMENTS = getPackageInfo()
if PKG_INFO["release"].startswith("a"):
    #classifiers.append("Development Status :: 1 - Planning")
    #classifiers.append("Development Status :: 2 - Pre-Alpha")
    classifiers.append("Development Status :: 3 - Alpha")
elif PKG_INFO["release"].startswith("b"):
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")
    #classifiers.append("Development Status :: 6 - Mature")
    #classifiers.append("Development Status :: 7 - Inactive")

gz = "{name}-{version}.tar.gz".format(**PKG_INFO)
PKG_INFO["download_url"] = (
    "{github_url}/releases/downloads/v{version}/{gz}"
    .format(gz=gz, **PKG_INFO)
)


def package_files(directory, prefix=".."):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        if "__pycache__" in path:
            continue
        for filename in filenames:
            if filename.endswith(".pyc"):
                continue
            paths.append(os.path.join(prefix, path, filename))
    return paths


if sys.argv[1:] and sys.argv[1] == "--release-name":
    print(PKG_INFO["release_name"])
    sys.exit(0)
else:
    # The extra command line options we added cause warnings, quell that.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Unknown distribution option")
        warnings.filterwarnings("ignore", message="Normalizing")
        setup(classifiers=classifiers,
              package_dir={"": "."},
              packages=find_packages(".",
                                     exclude=["tests", "tests.*"]),
              zip_safe=False,
              platforms=["Any"],
              keywords=["python", "application", "cookiecutter", "utils"],
              test_suite="./tests",
              include_package_data=True,
              package_data={
                  "nicfit": package_files("cookiecutter/"),
              },
              entry_points={
                  "console_scripts": [
                      "nicfit = nicfit.__main__:app.run",
                  ]
              },
              cmdclass={
                  "install": PipInstallCommand,
              },
              **PKG_INFO
        )

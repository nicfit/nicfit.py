#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import re
import sys
import warnings
from setuptools import setup, find_packages
from setuptools.command.install import install

classifiers = [
    "Intended Audience :: {{ cookiecutter.intended_audience }}",
    "Operating System :: POSIX",
    "Natural Language :: English",
{%- if cookiecutter.license == "MIT" %}
    "License :: OSI Approved :: MIT License",
{%- elif cookiecutter.license == "BSD-3" %}
    "License :: OSI Approved :: BSD License",
{%- elif cookiecutter.license == "GNU GPL v3.0" %}
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
{%- elif cookiecutter.license == "GNU GPL v2.0" %}
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
{%- elif cookiecutter.license == "GNU LGPL v3.0" %}
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
{%- elif cookiecutter.license == "GNU LGPL v2.0" %}
    "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
{%- elif cookiecutter.license == "Apache Software License 2.0" %}
    "License :: OSI Approved :: Apache Software License",
{%- elif cookiecutter.license == "Mozilla Public License 2.0" %}
    "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
{%- endif %}
    "Programming Language :: Python",
{%- if cookiecutter.py26 == "yes" %}
    "Programming Language :: Python :: 2.6",
{%- endif %}
{%- if cookiecutter.py27 == "yes" %}
    "Programming Language :: Python :: 2.7",
{%- endif %}
{%- if cookiecutter.py33 == "yes" %}
    "Programming Language :: Python :: 3.3",
{%- endif %}
{%- if cookiecutter.py34 == "yes" %}
    "Programming Language :: Python :: 3.4",
{%- endif %}
{%- if cookiecutter.py35 == "yes" %}
    "Programming Language :: Python :: 3.5",
{%- endif %}
{%- if cookiecutter.py36 == "yes" %}
    "Programming Language :: Python :: 3.6",
{%- endif %}
{%- if cookiecutter.py37 == "yes" %}
    "Programming Language :: Python :: 3.7",
{%- endif %}
{%- if cookiecutter.pyapp_type == "asyncio" %}
    "Framework :: AsyncIO",
{%- endif %}
    # XXX Remove to enable PyPi uploads
    "Private :: Do Not Upload",
]


def getPackageInfo():
    info_dict = {}
    info_keys = ["version", "name", "author", "author_email", "url", "license",
                 "description", "release_name", "github_url"]
    key_remap = {"name": "pypi_name"}

    # __about__
    info_fpath = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              "{{ cookiecutter.src_dir }}",
                              "{{ cookiecutter.py_module }}",
                              "__about__.py")
    with io.open(info_fpath, encoding='utf-8') as infof:
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
        with io.open("README.rst", encoding='utf-8') as readme_file:
            readme = readme_file.read()
    hist = "`changelog <{{ cookiecutter.github_url }}/blob/master/HISTORY.rst>`_"
    info_dict["long_description"] =\
        readme + "\n\n" +\
        "See the {} file for release history and changes.".format(hist)

    return info_dict, requirements


def requirements_yaml():
    prefix = "extra_"
    reqs = {}
    reqfile = os.path.join("requirements", "requirements.yml")
    if os.path.exists(reqfile):
        with io.open(reqfile, encoding='utf-8') as fp:
            curr = None
            for line in [l for l in [l.strip() for l in fp.readlines()]
                     if l and not l.startswith("#")]:
                if curr is None or line[0] != "-":
                    curr = line.split(":")[0]
                    reqs[curr] = []
                else:
                    assert line[0] == "-"
                    r = line[1:].strip()
                    if r:
                        reqs[curr].append(r.strip())

    return (reqs, {x[len(prefix):]: vals
                     for x, vals in reqs.items() if x.startswith(prefix)})


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
              package_dir={"": "{{ cookiecutter.src_dir }}"},
              packages=find_packages("{{ cookiecutter.src_dir }}",
                                     exclude=["tests", "tests.*"]),
              zip_safe=False,
              platforms=["Any"],
              keywords=["{{ cookiecutter.project_slug }}"],
              test_suite="{{ cookiecutter.src_dir }}/tests",
              include_package_data=True,
              package_data={},
              entry_points={
                  "console_scripts": [
                      "{{ cookiecutter.py_module }} = {{ cookiecutter.py_module }}.__main__:app.run",
                  ]
              },
              cmdclass={
                  "install": PipInstallCommand,
              },
              **PKG_INFO
        )

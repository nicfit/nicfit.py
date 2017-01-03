#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
from setuptools import setup, find_packages


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
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)
{%- elif cookiecutter.license == "GNU LGPL v2.0" %}
    "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
{%- elif cookiecutter.license == "Apache Software License 2.0" %}
    "License :: OSI Approved :: Apache Software License",
{%- elif cookiecutter.license == "Mozilla Public License 2.0" %}
    "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
{%- endif %}
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    # XXX Remove to enable PyPi uploads
    "Private :: Do Not Upload",
]


def getPackageInfo():
    info_dict = {}
    info_keys = ["version", "name", "author", "author_email", "url", "license",
                 "description", "release_name", "github_url"]
    key_remap = {"name": "project_name"}

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           "{{ cookiecutter.src_dir }}",
                           "{{ cookiecutter.py_module }}",
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

    vparts = info_dict["version"].split("-", maxsplit=1)
    info_dict["release"] = vparts[1] if len(vparts) > 1 else "final"
    return info_dict


readme = ""
if os.path.exists("README.rst"):
    with open("README.rst") as readme_file:
        readme = readme_file.read()

history = ""
if os.path.exists("HISTORY.rst"):
    with open("HISTORY.rst") as history_file:
        history = history_file.read().replace(".. :changelog:", "")


def requirements(filename):
    reqfile = os.path.join("requirements", filename)
    if os.path.exists(reqfile):
        return open(reqfile).read().splitlines()
    else:
        return ""


pkg_info = getPackageInfo()
if pkg_info["release"].startswith("a"):
    #classifiers.append("Development Status :: 1 - Planning")
    #classifiers.append("Development Status :: 2 - Pre-Alpha")
    classifiers.append("Development Status :: 3 - Alpha")
elif pkg_info["release"].startswith("b"):
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")
    #classifiers.append("Development Status :: 6 - Mature")
    #classifiers.append("Development Status :: 7 - Inactive")

gz = "{name}-{version}.tar.gz".format(**pkg_info)
pkg_info["download_url"] = (
    "{github_url}/releases/downloads/v{version}/{gz}"
    .format(gz=gz, **pkg_info)
)

if sys.argv[1:] and sys.argv[1] == "--release-name":
    print(pkg_info["release_name"])
    sys.exit(0)
else:
    setup(classifiers=classifiers,
          package_dir={"": "{{ cookiecutter.src_dir }}"},
          packages=find_packages("{{ cookiecutter.src_dir }}",
                                 exclude=["tests", "tests.*"]),
          zip_safe=False,
          platforms=["Any"],
          keywords=["{{ cookiecutter.project_slug }}"],
          include_package_data=True,
          install_requires=requirements("default.txt"),
          tests_require=requirements("test.txt"),
          test_suite="{{ cookiecutter.src_dir }}/tests",
          long_description=readme + "\n\n" + history,
          package_data={},
          entry_points={
              "console_scripts": [
                  "{{ cookiecutter.py_module }} = {{ cookiecutter.py_module }}.__main__:app.run",
              ]
          },
          **pkg_info
    )

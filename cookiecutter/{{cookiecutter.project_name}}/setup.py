#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
from setuptools import setup, find_packages


classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    # FIXME: make this conditional on License choice
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: POSIX",
    "Natural Language :: English",
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
                 "description", "release_name"]
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

src_dist_tgz = "{name}-{version}.tar.gz".format(**pkg_info)
# FIXME: this needs to be prompted for, and could use a better default anyway
pkg_info["download_url"] = "{}/releases/{}".format(pkg_info["url"],
                                                   src_dist_tgz)

if sys.argv[1] == "--release-name":
    print(pkg_info["release_name"])
    sys.exit(0)
else:
    setup(classifiers=classifiers,
          package_dir={"": "{{ cookiecutter.src_dir }}"},
          packages=find_packages("{{ cookiecutter.src_dir }}"),
          zip_safe=False,
          platforms=["Any",],
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

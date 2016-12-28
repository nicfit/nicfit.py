#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: POSIX',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
]


def getPackageInfo():
    info_dict = {}
    info_keys = ["version", "name", "author", "author_email", "url", "license",
                 "description", "release_name"]
    key_remap = {"name": "project_name"}

    base = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base, "nicfit/__about__.py")) as infof:
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
        history = history_file.read().replace('.. :changelog:', '')


def requirements(filename):
    reqfile = os.path.join("requirements", filename)
    if os.path.exists(reqfile):
        return open(reqfile).read().splitlines()
    else:
        return ""


pkg_info = getPackageInfo()

src_dist_tgz = "{name}-{version}.tar.gz".format(**pkg_info)
pkg_info["download_url"] = "{}/releases/{}".format(pkg_info["url"],
                                                   src_dist_tgz)

if sys.argv[1] == "--release-name":
    print(pkg_info["release_name"])
    sys.exit(0)
else:
    setup(classifiers=classifiers,
          package_dir={'nicfit.py': 'nicfit.py'},
          packages=find_packages('.', 'nicfit'),
          zip_safe=False,
          platforms=["Any",],
          keywords=['nicfit.py'],
          include_package_data=True,
          install_requires=requirements("default.txt"),
          tests_require=requirements("test.txt"),
          test_suite='tests',
          long_description=readme + '\n\n' + history,
          package_data={},
          entry_points={
              "console_scripts": [
                  "nicfit = nicfit.__main__:app.run",
              ]
          },
          **pkg_info
    )

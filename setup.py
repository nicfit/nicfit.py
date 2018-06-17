#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import re
import sys
import warnings
from pathlib import Path

from parcyl import Setup, setupAttrFromInfoFile

classifiers = [
    "Intended Audience :: Developers",
    "Operating System :: POSIX",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]


def getPackageInfo():
    info_dict = {}

    # Info
    readme = ""
    if os.path.exists("README.rst"):
        with io.open("README.rst", encoding='utf-8') as readme_file:
            readme = readme_file.read()
    hist = "`changelog <https://github.com/nicfit/nicfit.py/blob/master/HISTORY.rst>`_"
    info_dict["long_description"] =\
        readme + "\n\n" +\
        "See the {} file for release history and changes.".format(hist)

    return info_dict


about_file = Path(__file__).parent / "nicfit/__about__.py"
PKG_INFO = setupAttrFromInfoFile(about_file)
PKG_INFO.update(getPackageInfo())

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

        setup = Setup(packages=["."],
                      package_dir={"": "."},
                      exclude_packages=["tests", "tests.*"],
                      classifiers=classifiers,
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
                      **PKG_INFO
                     )
        setup()

#!/usr/bin/env python
import io
import os
import re
import sys
import warnings
from pathlib import Path

import parcyl

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

    # Info
    readme = ""
    if os.path.exists("README.rst"):
        with io.open("README.rst", encoding='utf-8') as readme_file:
            readme = readme_file.read()
    hist = "`changelog <{{ cookiecutter.github_url }}/blob/master/HISTORY.rst>`_"
    info_dict["long_description"] =\
        readme + "\n\n" +\
        "See the {} file for release history and changes.".format(hist)

    return info_dict


about_file = Path(__file__).parent / "nicfit/__about__.py"
PKG_INFO = parcyl.setupAttrFromInfoFile(about_file)
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

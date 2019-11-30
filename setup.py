#!/usr/bin/env python
from parcyl import Setup, find_package_files

setup = Setup(info_file="nicfit/__about__.py").with_packages(".", exclude=["test", "test.*"])
setup(package_dir={"": "."},
      zip_safe=False,
      platforms=["Any"],
      test_suite="./tests",
      include_package_data=True,
      package_data={
          "nicfit": find_package_files("cookiecutter/"),
          },
      entry_points={
                  "console_scripts": [
                      "nicfit = nicfit.__main__:app.run",
                  ]
              },
)

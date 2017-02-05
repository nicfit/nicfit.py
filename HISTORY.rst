Release History
===============

.. :changelog:

v0.5.9 (2017-02-04)
------------------------

New
~~~

- Load .cookiecutter.json enable migration.


v0.5.8 (2017-02-04)
------------------------

New
~~~

- Make clean-docs fix: cleaner setup with warning filter.
- Application.enableCommands top ease make subcmd type apps.
- Merging now done be 'nicfit cookiecutter'
- Better CC diff handling of new files. new: .gitignore ./tmp.

Fix
~~~

- Syntax error with LGPL3 choice.


v0.5.7 (2017-02-03)
------------------------

New
~~~

- Generate/save .cookiecutter.yml.
- git commit hook echo failed commit msg to screen for easy cut-n-paste.
- make doc-dist, removed _targets, etc.
- Pip cache for Travis-CI.

Fix
~~~

- Fixed docs Github pull request URL.


v0.5.6 (2017-02-02)
------------------------

New
~~~

- nicfit.console (moved from eyeD3)
- nicfit.util.cd (a chdir context manager)
- CommandError.exit_status.
- Added py37 support.

Changes
~~~~~~~

- Gitchangelog --author-format=email.
- Command.initAll raises a ValueError if no commands are registered.

Fix
~~~

- Fixed test for <=py35 missing features.
- Use command name for _all_commands.


v0.5.5 (2017-01-22)
------------------------

New
~~~
- Python version CC options.
- Docs.

Changes
~~~~~~~
- AUTHORS -> AUTHORS.rst.

Fix
~~~
- BROWSER usage for docs/coverage view targets.


v0.5.4 (2017-01-22)
------------------------

New
~~~
- 'nicfit cookiecutter'
- 'make build'
- Commands API (nicfit.command)

Fix
~~~
- Skip non-filed when CC diffing. [Travis Shirk]


v0.5.3 (2017-01-21)
-------------------

New
~~~
- Pluggable diff.
- Use CC_DIFF=yes to launch gvimdiff during 'make cookiecutter'
- Commit hook for enforcing gitchangelog formats.

Fix
~~~
- Support 1 or 2 digit version values. Fixes #3.

Other
~~~~~
- 'make changelog' [Travis Shirk]
- Cookiecut current branch, bitbucket and hg cleanup.


v0.5.2 (2014-01-14)
-------------------
* Initial release


v0.4.0 (2016-12-28)
-------------------

- Python 3.4 compatible.

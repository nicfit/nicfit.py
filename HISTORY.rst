Release History
===============

.. :changelog:
v0.6b0 (2017-06-23)
------------------------

New
~~~
- First class logger.
- Added an async Command.
- Add asyncio classifier when appropriate.

Changes
~~~~~~~
- Added pyaml and removed watchdog from dev.
- Gitchangelog 'show' argument was removed.

Fix
~~~
- Travis-CI, yay!
- Handle case where reqs files does not exist. Fixes #89.

Other
~~~~~
- Update chardet from 3.0.3 to 3.0.4 (#116) <github-bot@pyup.io>
- Update pytest from 3.1.1 to 3.1.2 (#117) <github-bot@pyup.io>
- Update pytest from 3.1.0 to 3.1.1 (#115) <github-bot@pyup.io>
- Update sphinx from 1.6.1 to 1.6.2 (#113) <github-bot@pyup.io>
- Update pytest-asyncio from 0.5.0 to 0.6.0 (#114) <github-bot@pyup.io>
- Merge branch 'master' of github.com:nicfit/nicfit.py.

  * 'master' of github.com:nicfit/nicfit.py:
    Update twine from 1.9.0 to 1.9.1 (#111)
    Update sphinx from 1.5.5 to 1.6.1 (#107)
- Update twine from 1.9.0 to 1.9.1 (#111) <github-bot@pyup.io>
- Update sphinx from 1.5.5 to 1.6.1 (#107) <github-bot@pyup.io>
- Inew: intl test.
- Update twine from 1.8.1 to 1.9.0 (#109) <github-bot@pyup.io>
- Update chardet from 3.0.2 to 3.0.3 (#108) <github-bot@pyup.io>
- Update pytest from 3.0.7 to 3.1.0 (#110) <github-bot@pyup.io>
- Update pytest-cov from 2.4.0 to 2.5.1 (#105) <github-bot@pyup.io>
- Update whichcraft from 0.4.0 to 0.4.1 (#103) <github-bot@pyup.io>
- Update ipdb from 0.10.2 to 0.10.3 (#101) <github-bot@pyup.io>
- Update pip-tools from 1.8.2 to 1.9.0 (#99) <github-bot@pyup.io>
- Update chardet from 2.3.0 to 3.0.2 (#97) <github-bot@pyup.io>
- Update binaryornot from 0.4.0 to 0.4.3. <github-bot@pyup.io>
- Pin pyaml to latest version 16.12.2. <github-bot@pyup.io>
- Merge branch 'master' of github.com:nicfit/nicfit.py.

  * 'master' of github.com:nicfit/nicfit.py:
    Update sphinx from 1.5.3 to 1.5.5 (#93)
    Update pip-tools from 1.8.1 to 1.8.2 (#90)
    Update babel from 2.3.4 to 2.4.0
    Update jinja2 from 2.9.5 to 2.9.6
    Update tox from 2.6.0 to 2.7.0
- Update sphinx from 1.5.3 to 1.5.5 (#93) <github-bot@pyup.io>
- Update pip-tools from 1.8.1 to 1.8.2 (#90) <github-bot@pyup.io>
- Update babel from 2.3.4 to 2.4.0. <github-bot@pyup.io>
- Update jinja2 from 2.9.5 to 2.9.6. <github-bot@pyup.io>
- Update tox from 2.6.0 to 2.7.0. <github-bot@pyup.io>
- Merge branch 'master' of github.com:nicfit/nicfit.py.

  * 'master' of github.com:nicfit/nicfit.py:
    Update poyo from 0.4.0 to 0.4.1
    Update pip-tools from 1.8.0 to 1.8.1
    Update curio from 0.6 to 0.7
    Update curio from 0.6 to 0.7
    Update pytest from 3.0.6 to 3.0.7
- Update poyo from 0.4.0 to 0.4.1. <github-bot@pyup.io>
- Update pip-tools from 1.8.0 to 1.8.1. <github-bot@pyup.io>
- Update curio from 0.6 to 0.7. <github-bot@pyup.io>
- Update curio from 0.6 to 0.7. <github-bot@pyup.io>
- Update pytest from 3.0.6 to 3.0.7. <github-bot@pyup.io>



v0.5.15 (2017-03-12)
------------------------

Changes
~~~~~~~
- Better __about__ version handling.

Other
~~~~~
- Add descriptions to subparsers, defaulting to the (short) help if not
  defined. <redshodan@gmail.com>
- Update markupsafe from 0.23 to 1.0. <github-bot@pyup.io>
- Update sphinx from 1.5.2 to 1.5.3. <github-bot@pyup.io>


v0.5.14 (2017-02-26)
------------------------

New
~~~
- Initial locale skel.


v0.5.13 (2017-02-25)
------------------------

New
~~~
- 'nicfit requirements' for generated requirements txt files.
- Clean up new unmerged files (fixes #17)

Changes
~~~~~~~
- Tox installs root requirements.txt.
- Less chatty gettext updates.
- No default gettext_domain.
- Removed detox.

Fix
~~~
- Less needless gettext updating.


v0.5.12 (2017-02-11)
------------------------

New
~~~
- gettext support (see nicfit.util.initGetText)
- ipdb and detox added in dev.txt

Fix
~~~
- Merging quoting fixes.


v0.5.11 (2017-02-05)
------------------------

New
~~~
- Nicfit cc --extra-merge.
- Don't CC merge src files that have not changed since last merge.
- Command aliases.

Changes
~~~~~~~
- Cleaned up logging opttions help and moved the large text to --help-
  logging.
- Move GITHUB var checks later in pre-release.

Fix
~~~
- TONs of tweaks.
- Better changelog tag ranges.


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

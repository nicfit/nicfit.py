Release History
===============

.. :changelog:

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

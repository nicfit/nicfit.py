Release History
===============

.. :changelog:

v0.6.6 (2017-10-10)
--------------------

New
~~~
- ConfigOpts.init_logging_fileConfig for invoking logging.config.fileConfig.
- :class:`nicfit.logger.FileConfig` supports instance creation and
  better utilities for updating config.
- The companion to ``getlist`` :meth:`Config.setlist`

Changes
~~~~~~~
- Pdb_opt (i.e. --pdb) is addded by default.

Fix
~~~
- <cmd> help <subcmd> works again.
- No f-strings in py35.

Other
~~~~~
- Update pyaml from 17.8.0 to 17.10.0 (#155) <github-bot@pyup.io>
- Update pytest from 3.2.2 to 3.2.3 (#154) <github-bot@pyup.io>
- Update tox from 2.8.2 to 2.9.1 (#153) <github-bot@pyup.io>
- Update pip-tools from 1.9.0 to 1.10.1 (#151) <github-bot@pyup.io>
- Update sphinx from 1.6.3 to 1.6.4 (#149) <github-bot@pyup.io>
- Update pytest-asyncio from 0.7.0 to 0.8.0 (#148) <github-bot@pyup.io>


v0.6.5 (2017-10-10)
------------------------

New
~~~
- ConfigOpts.init_logging_fileConfig for invoking
  logging.config.fileConfig.
- :class:`nicfit.logger.FileConfig` supports instance creation and
  better utilities for updating config.

  The static interface is on the way out.
- The companion to ``getlist`` :meth:`Config.setlist`

Changes
~~~~~~~
- Pdb_opt (i.e. --pdb)a addded by default.
- Python versin defaults and Trav-CI job ordering.

Fix
~~~
- <cmd> help <subcmd> works again.
- No f-strings in py35.

Other
~~~~~
- Merge branch 'master' of github.com:nicfit/nicfit.py.

  * 'master' of github.com:nicfit/nicfit.py:
    Update pyaml from 17.8.0 to 17.10.0 (#155)
- Update pyaml from 17.8.0 to 17.10.0 (#155) <github-bot@pyup.io>
- Merge branch 'master' of github.com:nicfit/nicfit.py.

  * 'master' of github.com:nicfit/nicfit.py:
    Update pytest from 3.2.2 to 3.2.3 (#154)
    Update tox from 2.9.0 to 2.9.1 (#153)
    fix: No f-strings in py35
    Update tox from 2.8.2 to 2.9.0 (#152)
    Update pip-tools from 1.9.0 to 1.10.1 (#151)
- Update pytest from 3.2.2 to 3.2.3 (#154) <github-bot@pyup.io>
- Update tox from 2.9.0 to 2.9.1 (#153) <github-bot@pyup.io>
- Update tox from 2.8.2 to 2.9.0 (#152) <github-bot@pyup.io>
- Update pip-tools from 1.9.0 to 1.10.1 (#151) <github-bot@pyup.io>
- Update sphinx from 1.6.3 to 1.6.4 (#149) <github-bot@pyup.io>
- Update pytest-asyncio from 0.7.0 to 0.8.0 (#148) <github-bot@pyup.io>



v0.6.5 (2017-09-21)
------------------------

Fix
~~~
- Typo for nicfit.py[cookiecutter] dev.txt requirement.



v0.6.4 (2017-09-18)
-------------------

New
~~~
- Added :func:`nicfit.command.register` decorator as class member to
  :class:`nicfit.command.Command`; less to import for convenience.
- Added ``nicfit[cookiecutter]`` to dev requirements.
- Docs use Sphinx_rtd_theme.

Changes
~~~~~~~
- Added README to dock title.
- Removed servedocs Makefile target.
- Use nicfit.py's ArgumentParser for subparsers and commands.
- Use ``print`` instead of logging for uncaught exceptions.

Other
~~~~~
- Update babel to 2.5.1 (#144) <github-bot@pyup.io>
- Update tox from 2.8.1 to 2.8.2 (#141) <github-bot@pyup.io>
- Update pytest-asyncio from 0.6.0 to 0.7.0 (#140) <github-bot@pyup.io>
- Update wheel from 0.29.0 to 0.30.0 (#142) <github-bot@pyup.io>
- Update pytest-runner from 2.12 to 2.12.1 (#138) <github-bot@pyup.io>
- Update pytest from 3.2.1 to 3.2.2 (#139) <github-bot@pyup.io>
- Update tox from 2.8.0 to 2.8.1 (#137) <github-bot@pyup.io>
- Pin deprecation to latest version 1.0.1 (#136) <github-bot@pyup.io>
- Pin pss to latest version 1.41 (#135) <github-bot@pyup.io>


v0.6.3 (2017-09-03)
--------------------

New
~~~
- :class:`nicfit.Config` has two new keyword args. ``touch=True`` to create
  default configs that do not exist and ``mode=int`` to set the file's perms.
- :class:`nicfit.ConfigOpts` has two new member ``extra_config_opts`` to enable
  passing additional kwargs when constructiong the ConfigClass.
  default configs that do not exist and ``mode=int`` to set the file's perms.
- :meth:`nicfit.Config.getlist` - Returns a list splitting on '\n' and ','
- New :class:`nicfit.logger.FileConfig` and :class:`nicfit.logger.DictConfig`
  classes for create default logging configs for root and package loggers.
- :class:`nicfit.Command` will create its own ArgumentParser if not
  provided a subparser. This makes the API usable for top-level commands.
- [cookiecutter] pytest-asyncio package is added as a dependency when the
  app type is asyncio.
- [cookiecutter] PyPy and PyPy3 cookiecutter options.
- [cookiecutter] Added ``pss`` and ``pyaml`` to dev requirements.

Fix
~~~
- Clean up cookiecutter temp dir.

Deprecation
~~~~~~~~~~~~
- :func:`nicfit.logger.LOGGING_CONFIG` deprecated in favor of
  :class:`nicfit.logger.FileConfig`


v0.6.2 (2017-08-26)
------------------------
- Cookiecutter updates.
- Update pyaml from 17.7.2 to 17.8.0 (#127) <github-bot@pyup.io>


v0.6.1 (2017-06-27)
------------------------

Fix
~~~
- Use os.path.expanduser/expandvars on config file arguments.


v0.6 (2017-06-24)
------------------------

New
~~~
- First class logger module.
- Added an asyncio Command.
- Add asyncio classifier when appropriate.

Changes
~~~~~~~
- Added pyaml and removed watchdog from dev.
- Gitchangelog 'show' argument was removed.

Fix
~~~
- Babel requirements.
- Travis-CI builds.
- Gettext tests
- Handle case where reqs files does not exist. Fixes #89.


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

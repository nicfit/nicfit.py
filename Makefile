.PHONY: clean-pyc clean-build clean-patch clean-local docs clean help lint \
	    test test-all coverage docs release dist tags
SRC_DIRS = nicfit.py tests bin
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "clean-patch - remove patch artifacts (.rej, .orig)"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo ""
	@echo "Options:"
	@echo "TEST_PDB - If defined PDB options are added when 'pytest' is invoked"

	@echo "BROWSER - Set to empty string to prevent opening docs/coverage results in a web browser"

clean: clean-local clean-build clean-pyc clean-test clean-patch
	rm -rf tags

clean-local:
	# TODO: Add extra clean targets here

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage

clean-patch:
	find . -name '*.rej' -exec rm -f '{}' \;
	find . -name '*.orig' -exec rm -f '{}' \;

lint:
	flake8 ${SRC_DIRS}


_PYTEST_OPTS=
ifdef TEST_PDB
    _PDB_OPTS=--pdb -s
endif

test:
	pytest $(_PYTEST_OPTS) $(_PDB_OPTS) ./tests

test-all:
	tox

_COVERAGE_BUILD_D=build/tests/coverage
coverage:
	# FIXME: write report to _COVERAGE_BUILD_D
	pytest --cov --cov-report=html ./tests

docs:
	rm -f docs/nicfit.py.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ nicfit.py
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@if test -n '$(BROWSER)'; then \
	    $(BROWSER) docs/_build/html/index.html;\
	fi

servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install

tags:
	ctags -R ${SRC_DIRS}

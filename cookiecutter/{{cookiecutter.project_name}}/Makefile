.PHONY: clean-pyc clean-build clean-patch clean-local docs clean help lint \
	    test test-all coverage docs release dist tags
SRC_DIRS = {{ cookiecutter.py_module }}
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
GIT := git -c user.name="$(NAME)" -c user.email="$(EMAIL)"
PYPI_REPO = pypitest

help:
	@echo "test - run tests quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "clean-patch - remove patch artifacts (.rej, .orig)"
	@echo "lint - check style with flake8"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "test-all - run tests on various Python versions with tox"
	@echo "release - package and upload a release"
	@echo "          PYPI_REPO=[pypitest]|pypi"
	@echo "pre-release - check repo and show version"
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
	flake8 $(SRC_DIRS)


{% if cookiecutter.use_pytest == "yes" -%}
_PYTEST_OPTS=
{%- else -%}
_NOSE_OPTS=--verbosity=1 --detailed-errors
{% endif %}
ifdef TEST_PDB
    _PDB_OPTS=--pdb -s
{%- if cookiecutter.use_pytest == "no" %}
    _PDB_OPTS+=--pdb-failures
{%- endif %}
endif

test:
{%- if cookiecutter.use_pytest == "yes" %}
	pytest $(_PYTEST_OPTS) $(_PDB_OPTS) ./tests
{%- else %}
	nosetests $(_NOSE_OPTS) $(_PDB_OPTS)
{% endif %}

test-all:
	tox

_COVERAGE_BUILD_D=build/tests/coverage
coverage:
	# FIXME: can these cover all SRC_DIRS?
{%- if cookiecutter.use_pytest == "yes" %}
	pytest --cov={{ cookiecutter.py_module }} --cov-report=html --cov-report term \
		   --cov-config=setup.cfg ./tests
{%- else %}
	nosetests $(_NOSE_OPTS) $(_PDB_OPTS) --with-coverage \
	      --cover-erase --cover-tests --cover-inclusive \
		  --cover-package={{ cookiecutter.py_module }} \
		  --cover-branches --cover-html \
		  --cover-html-dir=$(_COVERAGE_BUILD_D) tests
	@if test -n '$(BROWSER)'; then \
	    $(BROWSER) $(_COVERAGE_BUILD_D)/index.html;\
	fi
{% endif %}

docs:
	rm -f docs/{{ cookiecutter.project_slug }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ {{ cookiecutter.project_slug }}
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

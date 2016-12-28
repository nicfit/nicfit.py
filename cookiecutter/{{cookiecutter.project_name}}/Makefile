.PHONY: clean-pyc clean-build clean-patch clean-local docs clean help lint \
	    test test-all coverage docs release dist tags install \
	    build-release pre-release freeze-release _tag-release upload-release \
	    pypi-release github-release
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
NAME ?= {{ cookiecutter.full_name }}
EMAIL ?= {{ cookiecutter.email }}
GITHUB_USER ?= {{ cookiecutter.github_username }}
GITHUB_REPO ?= {{ cookiecutter.github_repo }}
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
	@# XXX Add new clean targets here.

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

{% if cookiecutter.use_pytest != "yes" %}
_COVERAGE_BUILD_D=build/tests/coverage
{% endif %}
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
	sphinx-apidoc -o docs/ {{ cookiecutter.py_module }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@if test -n '$(BROWSER)'; then \
	    $(BROWSER) docs/_build/html/index.html;\
	fi

servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

pre-release: test
	@test -n "${NAME}" || (echo "NAME not set, needed for git" && false)
	@test -n "${EMAIL}" || (echo "EMAIL not set, needed for git" && false)
	@test -n "${GITHUB_USER}" || (echo "GITHUB_USER not set, needed for github" && false)
	@test -n "${GITHUB_TOKEN}" || (echo "GITHUB_TOKEN not set, needed for github" && false)
	$(eval VERSION = $(shell python setup.py --version 2> /dev/null))
	@echo "VERSION: $(VERSION)"
	$(eval RELEASE_TAG = v${VERSION})
	@echo "RELEASE_TAG: $(RELEASE_TAG)"
	$(eval RELEASE_NAME = $(shell python setup.py --release-name 2> /dev/null))
	@echo "RELEASE_NAME: $(RELEASE_NAME)"
	git authors --list >| AUTHORS
	check-manifest

build-release: test-all dist

freeze-release:
	@($(GIT) diff --quiet && $(GIT) diff --quiet --staged) || \
	    (printf "\n!!! Working repo has uncommited/unstaged changes. !!!\n" && \
	     printf "\nCommit and try again.\n" && false)

_tag-release:
	$(GIT) tag -a $(RELEASE_TAG) -m "Release $(RELEASE_TAG)"
	$(GIT) push --tags origin

release: freeze-release pre-release build-release _tag-release upload-release

github-release: pre-release
	name="${RELEASE_TAG}"; \
    if test -n "${RELEASE_NAME}"; then \
        name="${RELEASE_TAG} (${RELEASE_NAME})"; \
    fi; \
    prerelease=""; \
    if echo "${RELEASE_TAG}" | grep '[^v0-9\.]'; then \
        prerelease="--pre-release"; \
    fi; \
    echo "NAME: $$name"; \
    echo "PRERELEASE: $$prerelease"; \
    github-release --verbose release --user "${GITHUB_USER}" \
                   --repo ${GITHUB_REPO} --tag ${RELEASE_TAG} \
                   --name "$${name}" $${prerelease}
	for file in $$(find dist -type f -exec basename {} \;) ; do \
        echo "FILE: $$file"; \
        github-release upload --user "${GITHUB_USER}" --repo ${GITHUB_REPO} \
                   --tag ${RELEASE_TAG} --name $${file} --file dist/$${file}; \
    done

upload-release: github-release pypi-release

pypi-release:
	find dist -type f -exec twine register -r ${PYPI_REPO} {} \;
	find dist -type f -exec twine upload -r ${PYPI_REPO} {} \;

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	@# The cd dist keeps the dist/ prefix out of the md5sum files
	cd dist && \
    for f in $$(ls); do \
        md5sum $${f} > $${f}.md5; \
    done
	ls -l dist

install: clean
	python setup.py install

tags:
	ctags -R ${SRC_DIRS}
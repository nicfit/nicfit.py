.PHONY: help build test clean dist install coverage pre-release release \
        docs clean-docs lint tags docs-dist docs-view coverage-view changelog \
        clean-pyc clean-build clean-patch clean-local clean-test-data \
        test-all test-data build-release freeze-release tag-release \
        pypi-release web-release github-release cookiecutter
SRC_DIRS = {{ cookiecutter.src_dir }}/{{ cookiecutter.py_module }}
TEST_DIR = {{ cookiecutter.src_dir }}/tests
TEMP_DIR ?= ./tmp
CC_DIR = ${TEMP_DIR}/{{ cookiecutter.project_name }}
NAME ?= {{ cookiecutter.full_name }}
EMAIL ?= {{ cookiecutter.email }}
{%- if cookiecutter.use_github == "yes" %}
GITHUB_USER ?= {{ cookiecutter.github_username }}
GITHUB_REPO ?= {{ cookiecutter.github_repo }}
{%- else %}
BITBUCKET_USER ?= {{ cookiecutter.bitbucket_username }}
BITBUCKET_REPO ?= {{ cookiecutter.bitbucket_repo }}
{%- endif %}
PYPI_REPO = pypitest
PROJECT_NAME = $(shell python setup.py --name 2> /dev/null)
VERSION = $(shell python setup.py --version 2> /dev/null)
RELEASE_NAME = $(shell python setup.py --release-name 2> /dev/null)
CHANGELOG = HISTORY.rst
CHANGELOG_HEADER = v${VERSION} ($(shell date --iso-8601))$(if ${RELEASE_NAME}, : ${RELEASE_NAME},)

help:
	@echo "test - run tests quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "clean-docs - remove autogenerating doc artifacts"
	@echo "clean-patch - remove patch artifacts (.rej, .orig)"
	@echo "build - byte-compile python files and generate other build objects"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "test-all - run tests on various Python versions with tox"
	@echo "release - package and upload a release"
	@echo "          PYPI_REPO=[pypitest]|pypi"
	@echo "pre-release - check repo and show version"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo "build - build package source files"
	@echo ""
	@echo "Options:"
	@echo "TEST_PDB - If defined PDB options are added when 'pytest' is invoked"
	@echo "BROWSER - HTML viewer used by docs-view/coverage-view"

build:
	python setup.py build

clean: clean-local clean-build clean-pyc clean-test clean-patch clean-docs
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
	rm -rf ${CC_DIR}

clean-patch:
	find . -name '*.rej' -exec rm -f '{}' \;
	find . -name '*.orig' -exec rm -f '{}' \;

lint:
	flake8 $(SRC_DIRS)

{% if cookiecutter.use_pytest == "yes" -%}
_PYTEST_OPTS=
{% else %}
_NOSE_OPTS=--verbosity=1 --detailed-errors
{%- endif %}
ifdef TEST_PDB
    _PDB_OPTS=--pdb -s
{%- if cookiecutter.use_pytest == "no" %}
    _PDB_OPTS+=--pdb-failures
{%- endif %}
endif

test:
{%- if cookiecutter.use_pytest == "yes" %}
	pytest $(_PYTEST_OPTS) $(_PDB_OPTS) ${TEST_DIR}
{%- else %}
	nosetests $(_NOSE_OPTS) $(_PDB_OPTS)
{%- endif %}

test-all:
	tox

{% if cookiecutter.use_pytest != "yes" %}
_COVERAGE_BUILD_D=build/tests/coverage
{% endif %}
coverage:
{%- if cookiecutter.use_pytest == "yes" %}
	pytest --cov={{ cookiecutter.src_dir }}/{{ cookiecutter.py_module }} \
           --cov-report=html --cov-report term \
           --cov-config=setup.cfg ${TEST_DIR}
{%- else %}
	nosetests $(_NOSE_OPTS) $(_PDB_OPTS) --with-coverage \
              --cover-erase --cover-tests --cover-inclusive \
              --cover-package={{ cookiecutter.src_dir }}/{{ cookiecutter.py_module }} \
              --cover-branches --cover-html \
              --cover-html-dir=$(_COVERAGE_BUILD_D) ${TEST_DIR}
{%- endif %}

coverage-view: coverage
	${BROWSER} build/tests/coverage/index.html;\

docs:
	rm -f docs/{{ cookiecutter.project_slug }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ ${SRC_DIRS}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

docs-view: docs
	$(BROWSER) docs/_build/html/index.html

docs-dist: clean-docs docs
	test -d dist || mkdir dist
	cd docs/_build && \
	    tar czvf ../../dist/${PROJECT_NAME}-${VERSION}_docs.tar.gz html

clean-docs:
	$(MAKE) -C docs clean
	-rm README.html

# FIXME: never been tested
servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

pre-release: lint test changelog
	@echo "VERSION: $(VERSION)"
	$(eval RELEASE_TAG = v${VERSION})
	@echo "RELEASE_TAG: $(RELEASE_TAG)"
	@echo "RELEASE_NAME: $(RELEASE_NAME)"
	check-manifest
{%- if cookiecutter.use_github == "yes" %}
	@if git tag -l | grep ${RELEASE_TAG} > /dev/null; then \
{%- else %}
	@if hg tags -q | grep ${RELEASE_TAG} > /dev/null; then \
{%- endif %}
        echo "Version tag '${RELEASE_TAG}' already exists!"; \
        false; \
    fi
{%- if cookiecutter.use_github == "yes" %}
	IFS=$$'\n';\
	for auth in `git authors --list`; do \
		echo "Checking $$auth...";\
		grep "$$auth" AUTHORS.rst || echo "* $$auth" >> AUTHORS.rst;\
	done
	@test -n "${GITHUB_USER}" || (echo "GITHUB_USER not set, needed for github" && false)
	@test -n "${GITHUB_TOKEN}" || (echo "GITHUB_TOKEN not set, needed for github" && false)
	@github-release --version    # Just a exe existence check
{%- else %}
	@# TODO: Update AUTHORS.rst file
	@# TODO: Check for tool for making bitbucket releases
{%- endif %}

changelog:
{%- if cookiecutter.use_github == "yes" %}
	last=`git tag -l --sort=version:refname | grep '^v[0-9]' | tail -n1`;\
	if ! grep "${CHANGELOG_HEADER}" ${CHANGELOG} > /dev/null; then \
		rm -f ${CHANGELOG}.new; \
		if test -n "$$last"; then \
			gitchangelog show --author-format=email $${last}..HEAD |\
			  sed "s|^%%version%% .*|${CHANGELOG_HEADER}|" |\
			  sed '/^.. :changelog:/ r/dev/stdin' ${CHANGELOG} \
			 > ${CHANGELOG}.new; \
		else \
			cat ${CHANGELOG} |\
			  sed "s/^%%version%% .*/${CHANGELOG_HEADER}/" \
			> ${CHANGELOG}.new;\
		fi; \
		mv ${CHANGELOG}.new ${CHANGELOG}; \
	fi
{%- else %}
	@# TODO
{%- endif %}

build-release: test-all dist

freeze-release:
{%- if cookiecutter.use_github == "yes" %}
	@# TODO: check for incoming
	@(git diff --quiet && git diff --quiet --staged) || \
{%- else %}
	@(test -z "`hg status --modified --added --deleted`" && \
      hg incoming | grep 'no changes found') || \
{%- endif %}
        (printf "\n!!! Working repo has uncommited/unstaged changes. !!!\n" && \
         printf "\nCommit and try again.\n" && false)

tag-release:
{%- if cookiecutter.use_github == "yes" %}
	git tag -a $(RELEASE_TAG) -m "Release $(RELEASE_TAG)"
	git push --tags origin
{%- else %}
	hg tag ${RELEASE_TAG}
	-hg commit -m "Release $(RELEASE_TAG)"
	hg push --rev .
{%- endif %}

release: pre-release freeze-release build-release tag-release upload-release

{% if cookiecutter.use_github == "yes" %}
github-release:
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
{% else %}
bitbucket-release:
	# Not implemented
	false
{%- endif %}

web-release:
	# TODO
	#find dist -type f -exec scp register -r ${PYPI_REPO} {} \;
	# Not implemented
	true

{% if cookiecutter.use_github == "yes" %}
upload-release: github-release pypi-release web-release
{% else %}
upload-release: bitbucket-release pypi-release web-release
{% endif %}

pypi-release:
	find dist -type f -exec twine register -r ${PYPI_REPO} {} \;
	find dist -type f -exec twine upload -r ${PYPI_REPO} --skip-existing {} \;

dist: clean docs-dist build
	python setup.py sdist --formats=gztar,zip
	python setup.py bdist_egg
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

README.html: README.rst
	rst2html5.py README.rst >| README.html
	if test -n "${BROWSER}"; then \
		${BROWSER} README.html;\
	fi

CC_DIFF ?= gvimdiff -geometry 169x60 -f
GIT_COMMIT_HOOK = .git/hooks/commit-msg
cookiecutter:
	rm -rf ${CC_DIR}
	if test "${CC_DIFF}" == "no"; then \
		nicfit cookiecutter --no-input ${TEMP_DIR}; \
		git -C ${CC_DIR} diff; \
		git -C ${CC_DIR} status -s -b; \
	else \
		nicfit cookiecutter --merge --no-input ${TEMP_DIR}; \
		if test ! -f ${GIT_COMMIT_HOOK}; then \
			touch ${GIT_COMMIT_HOOK}; \
		fi; \
		diff ${CC_DIR}/${GIT_COMMIT_HOOK} ${GIT_COMMIT_HOOK} >/dev/null || \
		     ${CC_DIFF} ${CC_DIR}/${GIT_COMMIT_HOOK} ${GIT_COMMIT_HOOK}; \
	fi

.PHONY: help build test clean dist install coverage pre-release release \
        docs clean-docs lint tags coverage-view changelog \
        clean-pyc clean-build clean-patch clean-local clean-test-data \
        test-all test-data build-release freeze-release tag-release \
        pypi-release web-release github-release cookiecutter requirements
SRC_DIRS = ./nicfit
TEST_DIR = ./tests
NAME ?= Travis Shirk
EMAIL ?= travis@pobox.com
GITHUB_USER ?= nicfit
GITHUB_REPO ?= nicfit.py
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
	@echo "pre-release - check repo and show version, generate changelog, etc."
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo "build - build package source files"
	@echo ""
	@echo "Options:"
	@echo "TEST_PDB - If defined PDB options are added when 'pytest' is invoked"
	@echo "BROWSER - HTML viewer used by docs-view/coverage-view"
	@echo "CC_MERGE - Set to no to disable cookiecutter merging."
	@echo "CC_OPTS - OVerrided the default options (--no-input) with your own."

build:
	python setup.py build
	${MAKE} -C ./cookiecutter all

clean: clean-local clean-build clean-pyc clean-test clean-patch clean-docs

clean-local:
	-rm tags
	${MAKE} -C ./cookiecutter clean
	-rm *.log
	rm -rf .cache

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find ./locale -name \*.mo -exec rm {} \;

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr .pytest_cache/

clean-patch:
	find . -name '*.rej' -exec rm -f '{}' \;
	find . -name '*.orig' -exec rm -f '{}' \;

lint:
	flake8 --builtins=_ $(SRC_DIRS)

_PYTEST_OPTS=
ifdef TEST_PDB
    _PDB_OPTS=--pdb -s
endif
test: gettext
	tox -e py37 -- $(_PYTEST_OPTS) $(_PDB_OPTS)

test-examples:
	true
	#for example in `ls ./examples/*.py`; do \
	#	echo "Running $$example..."; \
	#	./$$example > /dev/null ; \
	#done

test-all: gettext
	tox

coverage: gettext
	pytest --cov=./nicfit \
           --cov-report=html --cov-report term \
           --cov-config=setup.cfg ${TEST_DIR}

coverage-view: coverage
	${BROWSER} build/tests/coverage/index.html;\

docs:
	rm -f docs/nicfit.py.rst
	rm -f docs/modules.rst
	sphinx-apidoc -H $(PROJECT_NAME) -V $(VERSION) -o docs/ ${SRC_DIRS}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

docs-dist: docs
	test -d dist || mkdir dist
	cd docs/_build && \
	    tar czvf ../../dist/${PROJECT_NAME}-${VERSION}_docs.tar.gz html

docs-view: docs
	$(BROWSER) docs/_build/html/index.html

clean-docs:
	$(MAKE) -C docs clean
	-rm README.html

pre-release: clean lint test changelog requirements
	@# Keep docs off pre-release target list, else it is pruned during 'release' but
	@# after a clean.
	@$(MAKE) docs
	@echo "VERSION: $(VERSION)"
	$(eval RELEASE_TAG = v${VERSION})
	@echo "RELEASE_TAG: $(RELEASE_TAG)"
	@echo "RELEASE_NAME: $(RELEASE_NAME)"
	check-manifest
	@if git tag -l | grep -E '^$(shell echo ${RELEASE_TAG} | sed 's|\.|\\.|g')$$' > /dev/null; then \
        echo "Version tag '${RELEASE_TAG}' already exists!"; \
        false; \
    fi
	IFS=$$'\n';\
	for auth in `git authors --list | sed 's/.* <\(.*\)>/\1/'`; do \
		echo "Checking $$auth...";\
		grep "$$auth" AUTHORS.rst || echo "* $$auth" >> AUTHORS.rst;\
	done
	@test -n "${GITHUB_USER}" || (echo "GITHUB_USER not set, needed for github" && false)
	@test -n "${GITHUB_TOKEN}" || (echo "GITHUB_TOKEN not set, needed for github" && false)
	@github-release --version    # Just a exe existence check
	@git status -s -b

requirements:
	python -m nicfit requirements
	pip-compile -U requirements.txt -o ./requirements.txt

changelog:
	last=`git tag -l --sort=taggerdate | grep '^v[0-9]' | tail -n1`;\
	if ! grep "${CHANGELOG_HEADER}" ${CHANGELOG} > /dev/null; then \
		rm -f ${CHANGELOG}.new; \
		echo last: $$last;\
		if test -n "$$last"; then \
			gitchangelog --author-format=email --debug \
			             --omit-author="travis@pobox.com" $${last}..HEAD |\
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

build-release: test-all test-examples dist

freeze-release:
	@(git diff --quiet && git diff --quiet --staged) || \
        (printf "\n!!! Working repo has uncommited/unstaged changes. !!!\n" && \
         printf "\nCommit and try again.\n" && false)

tag-release:
	git tag -a $(RELEASE_TAG) -m "Release $(RELEASE_TAG)"
	git push --tags origin

release: pre-release freeze-release build-release twine-check tag-release upload-release

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
        echo "Uploading: $$file"; \
        github-release upload --user "${GITHUB_USER}" --repo ${GITHUB_REPO} \
                   --tag ${RELEASE_TAG} --name $${file} --file dist/$${file}; \
    done

web-release:
	@# Not implemented
	@true

upload-release: github-release pypi-release web-release

twine-check:
	@for f in `find dist -type f -name ${PROJECT_NAME}-${VERSION}.tar.gz \
              -o -name \*.egg -o -name \*.whl`; do \
        if test -f $$f ; then \
            twine check $$f ; \
        fi \
	done

pypi-release:
	for f in `find dist -type f -name ${PROJECT_NAME}-${VERSION}.tar.gz \
              -o -name \*.egg -o -name \*.whl`; do \
        if test -f $$f ; then \
            twine upload --verbose -r ${PYPI_REPO} --skip-existing $$f ; \
        fi \
	done

sdist: clean build
	python setup.py sdist --formats=gztar,zip

dist: clean gettext sdist docs-dist
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

CC_MERGE ?= yes
CC_OPTS ?= --no-input
GIT_COMMIT_HOOK = .git/hooks/commit-msg
cookiecutter:
	tmp_d=`mktemp -d`; cc_d=$$tmp_d/nicfit.py; \
	if test "${CC_MERGE}" == "no"; then \
		nicfit cookiecutter ${CC_OPTS} "$${tmp_d}"; \
		git -C "$$cc_d" diff; \
		git -C "$$cc_d" status -s -b; \
	else \
		nicfit cookiecutter --merge ${CC_OPTS} "$${tmp_d}" \
		       --extra-merge ${GIT_COMMIT_HOOK} ${GIT_COMMIT_HOOK};\
	fi; \
	rm -rf $$tmp_d

DEF_MSG_CAT = locale/en_US/LC_MESSAGES/nicfit.py.po
MSG_CAT_TMPL = locale/nicfit.py.pot

gettext-po:
	pybabel extract --no-location -o ${MSG_CAT_TMPL} -w 80 ${SRC_DIRS}
	test -f ${DEF_MSG_CAT} || \
		pybabel init -D nicfit.py -i ${MSG_CAT_TMPL}  -d locale -l en_US
	pybabel update -D nicfit.py -i ${MSG_CAT_TMPL}  -d locale

gettext:
	pybabel compile --statistics -D nicfit.py -d locale

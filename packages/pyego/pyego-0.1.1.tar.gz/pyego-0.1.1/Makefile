HELP="\
\#: == == == == == == == == == == == == == == == == == == == == == == == == == ==\n\
\#: MAKEFILE RECIPES\n\
\#:\n\
\#:    all:\n\
\#:        build documentation site and "build distribution"\n\
\#:\n\
\#:    init:\n\
\#:        create and/or activate virtual environment, and configure poetry\n\
\#:\n\
\#:    test:\n\
\#:        creates virtual environment, installs distribution, runs tests (via pytest)\n\
\#:\n\
\#:    sdist, resdist:\n\
\#:        build and rebuild "source distribution"\n\
\#:\n\
\#:    bdist, rebdist:\n\
\#:        build and rebuild "build distribution"\n\
\#:\n\
\#:    dist, redist:\n\
\#:        build and rebuild "source" and "build" distributions\n\
\#:\n\
\#:    show-sdist:\n\
\#:        print contents of "source distribution"\n\
\#:\n\
\#:    show-bdist:\n\
\#:        print contents of "build distribution"\n\
\#:\n\
\#:    show-dist:\n\
\#:        print contents of "source" and "build" distributions\n\
\#:\n\
\#:    docs:\n\
\#:        build documentation site\n\
\#:\n\
\#:    serve:\n\
\#:        serve documentation site on live server\n\
\#:\n\
\#:    dryrun.publish:\n\
\#:        rebuilds documentation, source and build distributions, then runs\n\
\#:        pre-publishing checks; stops right before actual publishing step.\n\
\#:\n\
\#:    publish:\n\
\#:        publishes source and build distributions to PyPI. make sure you've\n\
\#:        added your access token with '$$ poetry config pypi-token.pypi pypi-TOKENSECRET'.\n\
\#:\n\
\#: == == == == == == == == == == == == == == == == == == == == == == == == == ==\
"

SHELL=zsh
.SHELLFLAGS=-c

DIST_DIR=dist/
VIRTUALENV_DIR=venv/

DOCS_SITE=docs/site/
DOCS_SRC_FILES=$(shell find ./docs -type f ! -path './$(DOCS_SITE)*')
PYTHON_SRC_DIR=src/
PYTHON_SRC_FILES=$(shell find ./src -type f -path './$(PYTHON_SRC_DIR)*.py')

#: will have the name of the sdist/bdist if they exist, and so won't build, else won't and will build
SDIST=$(shell printf $(DIST_DIR)*.tar.gz)
BDIST=$(shell printf $(DIST_DIR)*.whl)

all: build.docs build.dist
re: fclean all

init:
	#: activate any existing virtual environments, else create one, activate it, and upgrade pip.
	if [[ -d .venv ]] \
	then \
		source .venv/**/bin/activate; \
	else; \
		mkdir -p .venv \
		&& /usr/bin/env python -m venv .venv \
		&& source .venv/bin/activate \
		&& pip install --upgrade pip \
		&& pip list; \
	fi
	@# https://github.com/python-poetry/poetry/issues/3353#issuecomment-804042557
	#: configure poetry
	poetry config virtualenvs.path --unset
	poetry config virtualenvs.in-project true
	poetry env use .venv/bin/python

#: run all defined tests for python distribution
test: init
	poetry install
	poetry run pytest

#: build only "source distribution" (sdist)
build.sdist: $(SDIST)
$(SDIST): $(PYTHON_SRC_FILES)
	poetry build --format sdist
#: rebuild only "source distribution" (sdist)
rebuild.sdist: clean-sdist build.sdist
#: show contents of sdist
show-sdist: build.sdist
	@echo 'Source Distribution (SDIST):'
	@tar --verbose --list --file $(DIST_DIR)*.tar.gz
	@echo

#: build only "build distribution" (bdist)
build.bdist: $(BDIST)
build.wheel: $(BDIST)
$(BDIST): $(PYTHON_SRC_FILES)
	poetry build --format wheel
#: rebuild only "build distribution" (bdist)
rebuild.bdist: clean-bdist build.bdist
#: show contents of bdist
show-bdist: build.bdist
	@echo '[Wheel] Built Distribution (BDIST):'
	@tar --verbose --list --file $(DIST_DIR)*.whl
	@echo

#: build both sdist and bdist
build.dist: build.sdist build.bdist
#: rebuild both sdist and bdist
rebuild.dist: clean-dist build.dist
#: show contents of both distributions
show: show-dist
show-all: show-dist
show-dist: build.dist show-sdist show-bdist

#: launch web server hosting documentation site
serve-docs:
	(poetry run sh -c 'cd docs/ && mkdocs serve')

#: build the documentation site in the local directory defined in ./docs/mkdocs.yaml in the field `site`
build.docs-site: $(DOCS_SITE)
$(DOCS_SITE): $(DOCS_SRC_FILES)
	(poetry run sh -c 'cd docs/ && mkdocs build')

#: dry-run publish distribution to PyPI
#: publish distribution to PyPI
dryrun.publish: re publish.checks
	poetry publish --dry-run
publish:
	poetry publish

#: clean sdist, bdist, and both distributions (hardcoded to avoid otherwise unexpected variable expansions, ... you never know)
clean-sdist:
	rm -rf ./dist/*.tar.gz
clean-bdist:
	rm -rf ./dist/*.whl
clean-dist:
	rm -rf ./dist/

#: clean dist. and environments
fclean: clean-dist
	rm -rf ./.venv/
	rm -rf ./docs/site/

help:
	@echo $(HELP)

.PHONY: all re sdist build.sdist resdist rebuild.sdist show-sdist bdist build.bdist wheel build.wheel rebdist rebuild.bdist show-bdist build dist build.dist rebuild redist rebuild.dist show show-all show-dist serve site docs build.docs-site dry-run-publish publish clean fclean help

#: ALIASES == == == == == == == == == == == == == == == == == == == == == == ==

sdist: build.sdist
resdist: rebuild.sdist
bdist: build.bdist
wheel: build.wheel
rebdist: rebuild.bdist
rebuild.wheel: rebuild.bdist
build: build.dist
dist: build.dist
rebuild: rebuild.dist
redist: rebuild.dist
serve: serve-docs
build.docs: build.docs-site
site: build.docs-site
docs: build.docs-site
docssite: build.docs-site
clean: clean-dist
publish.check.tests: test

#: UTILITIES == == == == == == == == == == == == == == == == == == == == == == ==

publish.checks: publish.check.tests publish.check.docs

publish.check.docs:
	@# if the source distribution doesn't contain the build documentation site, inform before publishing
	@if ! tar tf $(SDIST) | grep docs/site/ 1>/dev/null; then \
		printf "⚠️ Built documentation site is not present in the source distribution.\n"; \
		printf "Publish anyway? (y/N) "; \
		read </dev/tty; \
		case "$${REPLY}" in \
			y|Y|Yes|yes) : ;; \
			*) printf "Aborting publishing.\n"; exit 1 ;; \
		esac; \
	fi

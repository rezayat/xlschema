COLOR_BOLD_CYAN="\033[1;36m"
COLOR_RESET="\033[m"

section = @echo ${COLOR_BOLD_CYAN}">>> ${1}"${COLOR_RESET}

.PHONY: all

all: clean docs check coverage
	@echo "All DONE!"

# QUALITY
# -----------------------------------------------------------------------
.PHONY: check pylint flake8 radon proselint pyroma

check: pylint flake8 radon proselint
	$(call section,"checking quality")

pylint:
	$(call section,"running pylint")
	@python3 -m pylint src/xlschema


# DOCS
# -----------------------------------------------------------------------
.PHONY: docs uml html pdf

docs: clean-docs uml html

uml:
	$(call section,"building uml")
	@bash scripts/uml.sh

html:
	$(call section,"building html docs")
	@make -C docs html

pdf:
	$(call section,"building html docs")
	@make -C docs latexpdf


# STYLING
# -----------------------------------------------------------------------
.PHONY: style isort

style: isort

isort:
	$(call section,"isort")
	@isort --recursive src/xlschema/common
	@isort --recursive src/xlschema/ext
	@isort --recursive src/xlschema/fields
	@isort --recursive src/xlschema/plugins
	@isort --recursive src/xlschema/readers
	@isort --recursive src/xlschema/writers
	@isort src/xlschema/*.py

# TESTING
# -----------------------------------------------------------------------
.PHONY: test test-full test-fast test-time coverage

test: test-fast

coverage:
	$(call section,"coverage")
	@pytest --cov-report html:docs/coverage --cov=xlschema

test-full:
	$(call section,"test all")
	@pytest

test-fast:
	$(call section,"test skipping slowest tests")
	@pytest -k-slow

test-time:
	$(call section,"test all with top 20 slowest tests")
	@pytest --durations=20

test-html:
	$(call section,"test all with html report")
	@pytest --html=docs/test-report.html --self-contained-html


# CLEANING
# -----------------------------------------------------------------------
.PHONY: clean clean-pyc clean-output clean-tests clean-docs clean-build

clean: clean-pyc clean-output clean-tests clean-docs clean-build
	$(call section,"cleaning DONE")

clean-pyc:
	$(call section,"cleaning python artifacts")
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-build:
	$(call section,"cleaning build artifacts")
	@rm -rf build/
	@rm -rf dist/
	@rm -rf .eggs/
	@rm -rf *.egg-info

clean-docs:
	$(call section,"cleaning docs")
	@make -C docs clean >/dev/null

clean-tests:
	$(call section,"cleaning test files")
	@rm -rf .coverage .cache .hypothesis .pytest_cache

clean-output:
	$(call section,"cleaning output files")
	@rm -rf .xlschema/data/output/*
	@rm -rf tests/data/output/*
	@rm -rf ./output


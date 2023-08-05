.POSIX:

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: all venv build test deploy clean help
all: venv

$(VENV)/bin/activate: pyproject.toml
	python3 -m venv $(VENV)
	$(PIP) install -U pip wheel build
	# TODO: install dependencies and dev-dependencies

venv: $(VENV)/bin/activate ## Create virtual environment

build: venv ## Build python package
	$(PYTHON) -m build

test: venv ## Run tests
	$(PYTHON) -m pytest

deploy: venv build ## Deploy to PyPI
	$(PIP) install -U twine
	$(PYTHON) -m twine upload dist/* --verbose

clean: ## Clean environment (pycache, venv etc)
	rm -rf $(VENV) dist
	find . -type d -name "__pycache__" | xargs rm -r
	find . -type d -name "*.egg-info"  | xargs rm -r

# source: https://victoria.dev/blog/how-to-create-a-self-documenting-makefile/
help: ## Show this help
	@egrep -h "\s##\s" $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

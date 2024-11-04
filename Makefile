.DEFAULT_GOAL := help

SHELL=bash

ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    detected_OS := Windows
else
    # same as "uname -s"
    detected_OS := $(shell uname)
endif

.PHONY: fmt
fmt:  ## Run autoformatting and linting
	@pre-commit run --all-files

.PHONY: test
test:  ## Run tests
	@pytest

.PHONY: coverage
coverage:  ## Run tests and report coverage
	@coverage run -m pytest
	@coverage report --skip-empty

.PHONY: htmlcov
html: ## Run tests and create HTML coverage
	@coverage run -m pytest
	@coverage html

	@if [ "$(detected_OS)" = "Darwin" ]; then \
		open -a firefox htmlcov/index.html; \
	else \
		firefox htmlcov/index.html; \
	fi

.PHONY: clean
clean:  ## Clean up caches and build artifacts
	@rm -rf .mypy_cache/
	@rm -rf .pytest_cache/
	@rm -rf .ruff_cache/
	@rm -f .coverage
	@rm -rf htmlcov/
	@find . -type f -name '*.py[co]' -delete -or -type d -name __pycache__ -delete

.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort

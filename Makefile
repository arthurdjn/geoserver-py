.DEFAULT_GOAL := help

SRC:=geoserver
TESTS:=tests
CMD:=poetry run

# Linting, formatting, etc.

.PHONY: format
format: ## Format source code and tests
	$(CMD) ruff format $(SRC) $(TESTS)

.PHONY: lint
lint: ## Lint source code and tests
	$(CMD) ruff $(SRC) $(TESTS)

.PHONY: lint-fix
lint-fix: ## Lint and fix source code and tests
	$(CMD) ruff --fix $(SRC) $(TESTS)

.PHONY: type
type: ## Type in source code and tests
	$(CMD) mypy $(SRC) $(TESTS)

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	$(CMD) pre-commit run --all-files

.PHONY: all
all: format type lint isort ## Run all formatting commands

# Documentation

.PHONY: docs
docs: ## Generate documentation
	JUPYTER_PLATFORM_DIRS=1 $(CMD) mkdocs build

.PHONY: serve
serve: ## Serve documentation
	JUPYTER_PLATFORM_DIRS=1 $(CMD) mkdocs serve

# Tests

.PHONY: tests
tests: ## Run tests
	$(CMD) python -m pytest $(TESTS) -s -vv

# Versioning

.PHONY: show-bump
show-bump: ## Show available next versions
	$(CMD) bump-my-version show-bump

.PHONY: patch
patch: ## Bump version to next patch
	$(CMD) bump-my-version show --increment patch current_version new_version --format yaml
	$(CMD) bump-my-version bump patch

.PHONY: minor
minor: ## Bump version to next minor
	$(CMD) bump-my-version show --increment minor current_version new_version --format yaml
	$(CMD) bump-my-version bump minor

.PHONY: major
major: ## Bump version to next major
	$(CMD) bump-my-version show --increment major current_version new_version --format yaml
	$(CMD) bump-my-version bump major

# Utils

.PHONY: clean
clean: ## Clear local caches and build artifacts
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	rm -rf site
	rm -rf docs/_build
	rm -rf docs/.changelog.md docs/.version.md docs/.tmp_schema_mappings.html
	rm -rf coverage.xml
	rm -rf *.log

.PHONY: help
help: ## Show available commands
	@awk '/^[a-zA-Z0-9_-]+:.*?## .*$$/ { \
		helpCommand = substr($$0, 1, index($$0, ":")-1); \
		helpMessage = substr($$0, index($$0, "## ") + 3); \
		printf "\033[36m%-15s\033[0m %s\n", helpCommand, helpMessage; \
	}' $(MAKEFILE_LIST)

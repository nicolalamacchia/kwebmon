SOURCE = ./kwebmon_consumer

.PHONY: coverage
coverage: ## Show tests coverage
	pipenv run coverage run --source=$(SOURCE) -m unittest discover -s tests
	pipenv run coverage report -m

.PHONY: tests
tests: ## Run tests
	pipenv run python -m unittest discover -s tests

.PHONY: check-types
check-types: ## Run static type checking
	pipenv run mypy $(SOURCE)

.PHONY: lint
lint: ## Run the linter
	pipenv run flake8 $(SOURCE)

.PHONY: pydeps-dev
pydeps-dev: ## Install Python dependencies (dev)
	pipenv install --dev

.PHONY: pydeps-ci
pydeps-ci: ## Install Python dependencies (CI)
	pipenv install --deploy --dev

.PHONY: sysdeps
sysdeps: ## Install system dependencies
	pip install pipenv

.PHONY: ci-init
ci-init: ## Initialize CI environment
	pip install --upgrade pip
	make sysdeps
	make pydeps-ci

.PHONY: ci
ci: ## Run linter, type checking and tests
	make lint
	make check-types
	make tests

.PHONY: init
init: ## Initialize dev environment
	make sysdeps
	make pydeps-dev

.PHONY: run
run: ## Run kwebmon_consumer
	pipenv run python -m kwebmon_consumer

.DEFAULT_GOAL := help

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

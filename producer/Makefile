SOURCE = ./kwebmon_producer

.PHONY: coverage
coverage: ## Show tests coverage
	pipenv run coverage run --source=$(SOURCE) -m unittest discover -s tests
	pipenv run coverage report -m

.PHONY: tests
tests: ## Run tests
	pipenv run python -m unittest discover -s tests

.PHONY: lint
lint: ## Run the linter
	pipenv run flake8 $(SOURCE)

.PHONY: init
init: ## Initialize dev environment
	pip install pipenv
	pipenv install --dev

.DEFAULT_GOAL := help

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

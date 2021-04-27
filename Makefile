CONSUMER = consumer
PRODUCER = producer

.PHONY: coverage
coverage: ## Show tests coverage
	make -C $(CONSUMER) coverage
	make -C $(PRODUCER) coverage

.PHONY: tests
tests: ## Run tests
	make -C $(CONSUMER) tests
	make -C $(PRODUCER) tests

.PHONY: lint
lint: ## Run the linter
	make -C $(CONSUMER) lint
	make -C $(PRODUCER) lint

.PHONY: init
init: ## Initialize dev environment
	make -C $(CONSUMER) init
	make -C $(PRODUCER) init

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

#####
#
# Optional Input parameters
#
#####

# Integration or unit test target name. Specify with a target name to limit what test is run. Default will be all tests
TARGET ?=

# Integration or unit test python version. Specify to test with a specific python type. Default is the ansible-test default
PYTHON_VERSION ?= default

COLLECTION_ROOT ?= $(HOME)/.ansible/collections/ansible_collections/servicenow/itsm

.PHONY: help
help:
	@echo Available targets:
	@fgrep "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort

# Developer convenience targets
.PHONY: format
format:  ## Format python code with black
	black plugins tests/unit

.PHONY: clean
clean:  ## Remove all auto-generated files
	rm -rf tests/output

#####
#
# Test commands
#
#####
.PHONY: install-collection
install-collection:
	ansible-galaxy collection install --force -p ~/.ansible/collections .

## Run extra linter tests
.PHONY: linters
linters:
	@pip install -r linters.requirements.txt; err=0; echo "\nStart tests.\n"; \
	flake8 --select C90 --max-complexity 10 plugins || err=1; \
	black --check --diff --color plugins tests/unit extensions|| err=1; \
	if [ "$$err" = 1 ]; then echo "\nAt least one linter failed\n" >&2; exit 1; fi; \
	ansible-lint;

## Run sanity tests
.PHONY: sanity
sanity: install-collection linters
	cd $(COLLECTION_ROOT); \
	ansible-test sanity --docker

 ## Run unit tests
.PHONY: units
units: install-collection
	cd $(COLLECTION_ROOT); \
	ansible-test units --docker --coverage --python "$(PYTHON_VERSION)" $(TARGET); \
	ansible-test coverage combine --requirements --export tests/output/coverage/; \
	ansible-test coverage report --requirements --docker --omit 'tests/*' --show-missing

.PHONY: units-coverage
units-coverage: units
	cd $(COLLECTION_ROOT); \
	ansible-test coverage xml --requirements; \
	cp tests/output/reports/coverage.xml $(CURDIR)/coverage-units.xml;

## Run integration tests
.PHONY: integration
integration: install-collection
	cd $(COLLECTION_ROOT); \
	./tests/integration/generate_integration_config.sh; \
	ANSIBLE_ROLES_PATH=$(COLLECTION_ROOT)/tests/integration/targets \
		ANSIBLE_COLLECTIONS_PATH=~/.ansible/collections/ansible_collections \
		ansible-test integration --docker --diff --python "$(PYTHON_VERSION)" $(TARGET)

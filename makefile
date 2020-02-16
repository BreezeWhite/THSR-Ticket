
.PHONY: all
all: check test

.PHONY: check check-mypy check-flake check-pylint
check: check-mypy check-flake check-pylint

.PHONY: check-mypy
check-mypy:
	@echo "Checking typing..."
	@mypy --config-file .config/mypy.ini ./thsr_ticket/

.PHONY: check-flake
check-flake:
	@echo "Checking coding style..."
	@flake8 --config .config/flake ./thsr_ticket

.PHONY: check-pylint
check-pylint:
	@echo "Checking pylint"
	@pylint --rcfile .config/pylintrc ./thsr_ticket

.PHONY: test
test:
	@echo "Run unit tests"
	@python -m pytest ./thsr_ticket/unittest
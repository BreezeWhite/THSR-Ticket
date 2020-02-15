
.PHONY: all
all: check test

.PHONY: check check-mypy check-flake
check: check-mypy check-flake

.PHONY: check-mypy
check-mypy:
	@echo "Checking typing..."
	@mypy --config-file .config/mypy.ini thsr_ticket/

.PHONY: check-flake
check-flake:
	@echo "Checking coding style..."
	@flake8 --config .config/flake ./

.PHONY: test
test:
	@echo "Run unit tests"
	@python -m pytest ./thsr_ticket/unittest
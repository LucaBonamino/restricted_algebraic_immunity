PROJECT_NAME = algebraic_immunity

PYTHON = python

M = $(shell printf "\033[34;1m▶\033[0m")

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available targets:"
	@echo "$(M) help          - Display this help message"
	@echo "$(M) setup          - Install package"
	@echo "$(M) deps          - Install dependencies"

.PHONY: setup
setup:
	@$(info $(M) installing package)
	pip install .

.PHONY: setup-dev
setup-dev:
	@$(info $(M) installing package)
	pip install -e .

.PHONY: uninstall
uninstall:
	@$(info $(M) installing package)
	pip-autoremove ${PROJECT_NAME} -y
	pip3 uninstall ${PROJECT_NAME}


.PHONY: deps
deps:
	@$(info $(M) installing dependencies...)
	pip install -r requirements.txt

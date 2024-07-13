all: commands

## dev: rebuild development version of package
.PHONY: dev
dev:
	pip install -e .

## lint: check code using ruff
.PHONY: lint
lint:
	@ruff check snailz

## clean: remove datafiles
.PHONY: clean
clean:
	@find . -name '*~' -exec rm {} \;
	@find . -type d -name __pycache__ | xargs rm -r
	@find . -type d -name .pytest_cache | xargs rm -r
	@rm -rf ./data/*
	@mkdir -p ./data
	@touch ./data/.touch

## ---: ---

include snailz/Makefile

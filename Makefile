REPO_ROOT := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))


.PHONY: clean build install man-diff man-update demo test-version test-code


clean:
	@rm -rf ./dist/

build:
	@poetry build --format=sdist

install:
	@poetry install

man-diff:
	@poetry run python ./housekeeping-scripts/diff-man-pages.py \
		$(REPO_ROOT)/fzf.1.man

man-update:
	@./housekeeping-scripts/update-man-pages.sh

demo:
	@poetry run python -m fzf_but_typed demo

test-version:
	@poetry run python -m fzf_but_typed compatibility

test-code:
	@poetry run pytest

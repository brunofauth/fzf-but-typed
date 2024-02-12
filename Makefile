REPO_ROOT := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))


.PHONY: clean build install man-diff man-update demo test


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
	@poetry run python -m fzf_but_typed

test:
	@poetry run pytest

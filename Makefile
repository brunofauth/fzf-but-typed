REPO_ROOT := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))


.PHONY: edit
edit:
	@find src/fzf_but_typed -type f -name *.py -and -not -name __init__.py | xargs --open-tty poetry run vim

.PHONY: clean
clean:
	@rm -rf ./dist/

.PHONY: build
build:
	@poetry build --format=sdist

.PHONY: publish
publish:
	@make build
	@twine upload --repository pypi --skip-existing --verbose --username __token__ --password $(shell /bin/sh -c 'pass pypi.org/token | head -n 1') dist/* 

.PHONY: install
install:
	@poetry install

.PHONY: man-diff
man-diff:
	@poetry run python ./housekeeping-scripts/diff-man-pages.py \
		$(REPO_ROOT)/fzf.1.man

.PHONY: man-update
man-update:
	@./housekeeping-scripts/update-man-pages.sh

.PHONY: demo
demo:
	@poetry run python -m fzf_but_typed

.PHONY: test
test:
	@poetry run pytest

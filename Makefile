.PHONY: clean man-diff man-update demo test-version test-code


clean:
	@rm -rf ./dist/

build:
	@poetry build --format=sdist

man-diff:
	@./housekeeping-scripts/diff-man-pages.sh

man-update:
	@./housekeeping-scripts/update-man-pages.sh

demo:
	@poetry run python -m fzf_but_typed demo

test-version:
	@poetry run python -m fzf_but_typed compatibility

test-code:
	@poetry run pytest

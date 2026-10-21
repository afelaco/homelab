.PHONY: bootstrap
bootstrap:
	bash ./bootstrap/main.sh

pre-commit-autoupdate:
	uv run pre-commit autoupdate

pre-commit-install:
	uv run pre-commit install

pre-commit-run:
	uv run pre-commit run --all-files

ruff-format:
	uv run ruff format

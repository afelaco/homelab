.PHONY: bootstrap
bootstrap:
	bash ./bootstrap/main.sh

pre-commit-autoupdate:
	uv run pre-commit autoupdate

pre-commit-run:
	uv run pre-commit run --all-files

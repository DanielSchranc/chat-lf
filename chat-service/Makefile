.PHONY: test test-all lint format

test:
	poetry run pytest -m unit -v

test-all:
	poetry run pytest -v

lint:
	poetry run ruff check .

format:
	poetry run black .

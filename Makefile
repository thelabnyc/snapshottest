all: install test

.PHONY: develop
develop: install

.PHONY: install
install:
	uv sync

.PHONY: test
test:
# Run Pytest tests (including examples)
	uv run py.test tests examples/pytest

# Run Unittest Example
	uv run python examples/unittest/test_demo.py

# Run nose2
	uv run nose2 examples.unittest

# Run Django Example
	cd examples/django_project && uv run python manage.py test

.PHONY: lint
lint:
	uv run ruff check
	uv run ruff format --check

.PHONY: clean
clean:
	rm -rf dist/ build/

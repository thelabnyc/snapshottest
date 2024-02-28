all: install test

.PHONY: develop
develop: install

.PHONY: install
install:
	poetry install

.PHONY: test
test:
# Run Pytest tests (including examples)
	poetry run py.test --cov=snapshottest tests examples/pytest

# Run Unittest Example
	poetry run python examples/unittest/test_demo.py

# Run nose2
	poetry run nose2 examples.unittest

# Run Django Example
	cd examples/django_project && poetry run python manage.py test

.PHONY: lint
lint:
	flake8

.PHONY: clean
clean:
	rm -rf dist/ build/

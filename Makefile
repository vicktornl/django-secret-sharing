.PHONY: default clean format install coverage test dist

default: clean format install dist

clean:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +

format:
	ruff check . --fix
	ruff format

install:
	pip install -e .[test,aws]

coverage:
	coverage run -m pytest
	coverage html
	coverage report -m

test:
	pytest --reuse-db

dist:
	pip install --upgrade build twine
	python -m build
	twine check dist/*
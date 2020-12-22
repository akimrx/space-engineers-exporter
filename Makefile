.PHONY: clean clean-build clean-pyc dist help
.DEFAULT_GOAL := help

help:
	@echo "clean - remove all artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove python artifacts"
	@echo "install - install the package"
	@echo "init - initialize the development environment"
	@echo "dist - build package"
	@echo "release - upload package to PyPi"
	@echo "pep8 - check style with pep8"
	@echo "black - check style with black"
	@echo "lint - check style with pylint"
	@echo "sort - sorting imports"

clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '.DS_Store' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

pep8:
	flake8 se_exporter

lint:
	pylint --rcfile=setup.cfg se_exporter

black:
	black --check --color --diff -l 100 .

sort:
	isort .

dist:
	python3 setup.py sdist bdist_wheel

release: dist
	@make dist
	python3 -m twine upload --repository pypi dist/*

install: clean
	python3 setup.py install

init:
	pip3 install -r requirements-dev.txt
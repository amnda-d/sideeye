.PHONY: clean build lint test help

clean:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f  {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@rm -rf *.egg-info

lint:
	pylint sideeye --disable=too-few-public-methods,too-many-arguments --output-format=colorized || true

build: clean
	pip install -e .[test]

test: build
	make lint
	cd tests
	-nose2 -c tests/nose2.cfg -v --layer-reporter
	cd ..
	make clean

help:
	@echo "		clean"
	@echo "		  Remove python artifacts."
	@echo "		lint"
	@echo "		  Check style with pylint."
	@echo "		test"
	@echo "		  Run nose2 tests"
	@echo "		build"
	@echo "		  Clean artifacts and rebuild package"

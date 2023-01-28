PATH := $(shell pwd)/bin:$(PATH)
$(shell cp -n dev.env .env)
include .env

install: build
	#pip install -r requirements.pip

build:
	docker build -t "$(PYTHON_DEV_IMAGE):$(REVISION)" .

test:
	python -m unittest discover tests/

coverage:
	coverage run -m unittest discover tests/ && coverage html

lint-check:
	pylint src/ tests/

lint-fix:
	python -m black .

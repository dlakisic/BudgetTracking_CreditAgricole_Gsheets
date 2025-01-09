.PHONY: install test lint deploy

install:
	pip install -r requirements.txt

test:
	pytest

lint:
	flake8 .
	black . --check

format:
	black .

deploy:
	serverless deploy 
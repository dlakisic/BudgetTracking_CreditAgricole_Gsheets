.PHONY: install test lint deploy clean package zip

install:
	pip install -r requirements.txt

test:
	pytest

lint:
	flake8 .
	black . --check

format:
	black .

clean:
	rm -rf package/
	rm -rf .serverless/
	rm -f lambda.zip
	find . -type d -name __pycache__ -exec rm -rf {} +

package: clean
	mkdir -p package
	pip install -r requirements.txt -t package/
	cp -r utils package/
	cp lambda_function.py package/

zip: package
	cd package && zip -r ../lambda.zip . && cd .. 
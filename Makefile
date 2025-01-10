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
	python -m venv .venv-lambda
	. .venv-lambda/bin/activate && \
	pip install \
		fastapi==0.115.6 \
		mangum==0.19.0 \
		pydantic==2.10.5 \
		boto3==1.35.96 \
		pandas==2.2.3 \
		gspread==6.1.4 \
		oauth2client==4.1.3 \
		creditagricole_particuliers==0.14.3 \
		-t package/
	deactivate
	rm -rf .venv-lambda
	cp -r utils package/
	cp lambda_function.py package/

zip: package
	cd package && zip -r ../lambda.zip . && cd ..
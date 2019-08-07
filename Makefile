test:
	pytest

clean:
	rm meetup-notifier-lambda.zip || true

lambdify: test clean
	pip install -r ./requirements.txt -t . --upgrade && zip -r meetup-notifier-lambda.zip .

.PHONY: test

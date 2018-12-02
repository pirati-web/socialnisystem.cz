
init-env:
	python3 -m venv .env

install:
	pip install pip-tools && pip install --upgrade -r requirements.txt && npm install

install-test:
	pip install --upgrade -r requirements-test.txt

run:
	DEBUG=1 ./node_modules/.bin/concurrently -r -k "python manage.py runserver 8080" "./node_modules/.bin/webpack --config webpack.config.js --mode development --watch"

dep-freeze:
	pip-compile requirements.in

test:
	pytest

migrate:
	DEBUG=1 python manage.py migrate

build:
	docker build -t xaralis/socialsystem:latest .

push:
	docker push xaralis/socialsystem:latest

release:
	make build
	make push

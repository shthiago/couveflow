lint:
	pylint --django-settings-module=couveflow.settings couveflow/

format:
	isort .

test:
	docker-compose -f docker-compose-dev.yml run web  pytest -vvv --cov=couveflow couveflow/

run-dev:
	docker-compose -f docker-compose-dev.yml up

build:
	docker-compose -f docker-compose-dev.yml build

migrate:
	docker-compose -f docker-compose-dev.yml run web python manage.py migrate
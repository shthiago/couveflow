lint:
	pylint --django-settings-module=couveflow.settings couveflow/

format:
	isort .

test:
	pytest -vvv --cov=couveflow couveflow/

run-dev:
	python manage.py runserver 0:8000
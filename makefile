lint:
	pylint --django-settings-module=couveflow.settings couveflow/

test:
	pytest --cov=couveflow couveflow/

run-dev:
	python manage.py runserver 0:8000
FROM python:3.10-bullseye

# Install poetry
RUN pip install poetry

EXPOSE 8000

WORKDIR /opt
COPY pyproject.toml poetry.lock /

# Setup environment
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --only main

WORKDIR /opt
ADD couveflow/ couveflow/
ADD scripts/ scripts/
ADD manage.py manage.py 

CMD ["./scripts/entrypoint.sh"]
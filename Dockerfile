FROM python:3.9

ENV FLASK_APP todo_api
RUN pip install poetry
COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install

COPY . ./

CMD ["uwsgi", "--ini", "wsgi.ini"]

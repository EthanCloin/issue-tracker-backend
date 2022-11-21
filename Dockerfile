FROM python:3.10 as requirements-stage
WORKDIR /tmp
# convert pyproject into requirements in requirements stage
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# main build stage
FROM python:3.10
WORKDIR /src
COPY --from=requirements-stage /tmp/requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app

CMD [ "uvicorn", "app.api.v1.issue_service:app", "--host", "0.0.0.0", "--port", "8000" ]
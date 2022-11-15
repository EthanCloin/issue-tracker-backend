FROM python:3.10-alpine as requirements-stage
WORKDIR /tmp
# convert pyproject into requirements in requirements stage
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# main build stage
FROM python:3.10-alpine
WORKDIR /src
COPY --from=requirements-stage /tmp/requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app

CMD [ "python", "-m", "app.console" ]
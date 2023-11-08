FROM python:3.11.4

# set work directory
WORKDIR trading_fastAPI

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update
RUN apt-get install -y curl

# install dependencies
COPY pyproject.toml poetry.lock ./

# copy project & entrypointscripts
COPY ./src ./src

ADD entrypoint-fastapi.sh ./
ADD entrypoint-celery-worker.sh ./
ADD entrypoint-celery-schedule.sh ./

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry install

# Give execute permissions to the entrypoint script
RUN chmod +x ./entrypoint-fastapi.sh

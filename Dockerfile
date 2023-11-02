FROM python:3.11.4

# set work directory
WORKDIR trading_fastAPI

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y curl

# install dependencies
COPY pyproject.toml poetry.lock ./

# copy project & entrypointscripts
COPY ./src ./src

ADD entrypoint-fastapi.sh ./

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry install

# Give execute permissions to the entrypoint script
RUN chmod 777 ./entrypoint-fastapi.sh

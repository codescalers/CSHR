# FROM python:3.8.10-slim-buster AS development_build
FROM ubuntu:20.04

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.0.5 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
# System deps:
RUN apt-get update && apt-get install -y openssh-server nginx python3.8 python3-pip \
    && pip install "poetry==$POETRY_VERSION" && poetry --version

# set work directory
WORKDIR /server
COPY pyproject.toml poetry.lock /server/

# Install dependencies:
RUN poetry install
# copy project
COPY . .

EXPOSE 8000
RUN chmod +x /server/start.sh
CMD ["python3","./manage.py", "runserver", "0.0.0.0:8000"]
# docker run --name <container_name> -p 8000:8000 -d <image_name>

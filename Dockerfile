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
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
# set work directory
WORKDIR /server_directory
COPY . /server_directory

# System deps:
RUN apt-get update && apt-get install -y openssh-server nginx python3.8 python3-pip \
    && pip install "poetry==$POETRY_VERSION" && poetry --version

# Install zinit.
# RUN wget -O /sbin/zinit https://github.com/threefoldtech/zinit/releases/download/v0.2.5/zinit
# COPY zinit /etc/zinit
# && chmod +x /sbin/zinit

# Install dependencies:
RUN poetry install

EXPOSE 8000
# change start.sh mode.
RUN chmod +x /server_directory/start.sh
CMD ["python3","./manage.py", "runserver", "0.0.0.0:8000"]
# docker run --name <container_name> -p 8000:8000 -d <image_name>

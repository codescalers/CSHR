FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC \
    DJANGO_DEBUG=DJANGO_DEBUG \
    DJANGO_SECRET_KEY=DJANGO_SECRET_KEY \
    EMAIL_HOST=EMAIL_HOST EMAIL=EMAIL \
    EMAIL_PASSWORD=EMAIL_PASSWORD \
    REDIS_HOST=REDIS_HOST CLIENT_IP="127.0.0.2"

RUN mkdir -p /etc/zinit/
RUN echo deb http://be.archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse >> /etc/apt/sources.list
RUN apt-get -y update && \
    apt-get -y install wget vim openssh-client openssh-server python3.8 python3-pip \
    vim && rm -rf /var/lib/apt/lists/*

RUN wget -O /sbin/zinit https://github.com/threefoldtech/zinit/releases/download/v0.2.5/zinit && \
  chmod +x /sbin/zinit && pip install poetry && poetry --version


WORKDIR /server_dir
COPY . /server_dir
COPY zinit /etc/zinit

RUN chmod +x /server_dir/start.sh
RUN poetry install
RUN poetry run python3 manage.py makemigrations
RUN poetry run python3 manage.py migrate

EXPOSE 8000
ENTRYPOINT  ["zinit", "init"]
FROM ubuntu:22.04

# Set the environment variable
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
ENV REDIS_HOST=$REDIS_HOST
ENV DJANGO_DEBUG=$DJANGO_DEBUG
ENV EMAIL=$EMAIL
ENV EMAIL_PASSWORD=$EMAIL_PASSWORD
ENV EMAIL_HOST=$EMAIL_HOST
ENV DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL
ENV DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
ENV SERVER_DOMAIN_NAME=$SERVER_DOMAIN_NAME
ENV CLIENT_DOMAIN_NAME=$CLIENT_DOMAIN_NAME

RUN mkdir -p /etc/zinit/
RUN echo deb http://be.archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse >> /etc/apt/sources.list
RUN apt-get -y update && \
    apt-get -y install wget sudo redis ufw vim openssh-client openssh-server python3.8 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /server_dir

RUN wget -O /sbin/zinit https://github.com/threefoldtech/zinit/releases/download/v0.2.5/zinit && \
  chmod +x /sbin/zinit && pip install poetry && poetry --version

COPY . /server_dir
COPY server/zinit /etc/zinit

RUN chmod +x server/scripts/*.sh
EXPOSE 8000
ENTRYPOINT  ["zinit", "init"]
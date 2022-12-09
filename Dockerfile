FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC

RUN mkdir -p /etc/zinit/
RUN echo deb http://be.archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse >> /etc/apt/sources.list
RUN apt-get -y update && \
    apt-get -y install wget sudo ufw vim openssh-client openssh-server python3.8 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /server_dir

RUN wget -O /sbin/zinit https://github.com/threefoldtech/zinit/releases/download/v0.2.5/zinit && \
  chmod +x /sbin/zinit && pip install poetry && poetry --version


COPY . /server_dir
COPY server/zinit /etc/zinit

RUN chmod +x server/scripts/*.sh
EXPOSE 8000
ENTRYPOINT  ["zinit", "init"]
FROM ubuntu:22.04
RUN echo deb http://be.archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse >> /etc/apt/sources.list
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Europe/Belgium apt-get install -y openssh-client openssh-server git mc mcedit curl wget dnsutils iproute2 vim && rm -rf /var/lib/apt/lists/*

WORKDIR /server_directory
COPY . /server_directory

RUN chmod +x /server_directory/init.sh
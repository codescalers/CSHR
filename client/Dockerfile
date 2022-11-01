FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC

RUN mkdir -p /etc/zinit/
RUN echo deb http://be.archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse >> /etc/apt/sources.list
RUN apt-get -y update && \
    apt-get -y install wget vim openssh-client openssh-server nginx nodejs npm && \
    rm -rf /var/lib/apt/lists/*

RUN wget -O /sbin/zinit https://github.com/threefoldtech/zinit/releases/download/v0.2.5/zinit && \
  chmod +x /sbin/zinit

WORKDIR /client_dir
COPY . /client_dir
COPY zinit /etc/zinit

RUN chmod +x /client_dir/start.sh

EXPOSE 8080
ENV HOST=0.0.0.0
ENTRYPOINT ["zinit", "init"]

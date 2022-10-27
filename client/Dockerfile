FROM node:12 AS build

ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
WORKDIR /client_dir
COPY . /client_dir

RUN apt-get -y update && \
    apt-get -y install wget curl vim nginx openssh-client openssh-server && \
    rm -rf /var/lib/apt/lists/*

RUN wget -O /sbin/zinit https://github.com/threefoldtech/zinit/releases/download/v0.2.5/zinit && \
  chmod +x /sbin/zinit && chmod +x /client_dir/start.sh

COPY zinit /etc/zinit

RUN npm run build
EXPOSE 8080

ENV HOST=0.0.0.0

ENTRYPOINT ["zinit", "init"]

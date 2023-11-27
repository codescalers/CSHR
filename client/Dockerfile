FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    NVM_DIR=/usr/local/nvm \
    NODE_VERSION=18.0.0 \
    HOST=0.0.0.0 \
    PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH \
    NODE_PATH=$NVM_DIR/v$NODE_VERSION/lib/node_modules

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Update the repository sources list and install dependencies
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get -y autoclean

# Install nvm
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash

# Install Node.js and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && npm install -g yarn

# Install other dependencies
RUN apt-get -y update && \
    apt-get -y install wget vim openssh-client openssh-server nginx nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# Install zinit
RUN wget -O /sbin/zinit https://github.com/threefoldtech/zinit/releases/download/v0.2.5/zinit && \
    chmod +x /sbin/zinit

WORKDIR /client_dir
COPY . /client_dir
COPY zinit /etc/zinit

RUN chmod +x /client_dir/scripts/*.sh

EXPOSE 8080
ENTRYPOINT ["zinit", "init"]

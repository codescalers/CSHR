FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC SSH_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC8KhnjC8yi2Td7gMEiVmJfUNg1lXE457S+eW1jip0HW3MGLsKjXekauLbR7qcSOKUGURZlsw2KbRdOZnWbQovs24YdevUos/9XIHxFL+mJEy+5gyHuU5Z/yGcuW7O6Qj5xtwvBwe/kWnMtgEd2xXxQqEY3ZHkVh++mA/eqbhikMIsM7Qi5SKBT210+7KT5989BbUpk9e43koFNkVPCXgDR5+frhbEvCq06OVAE8vuEQ/C6EW1ZKn65nVt2z0kA7c8rUE0sEZRnI35oCEwazMlxiPm9B67GryoO7bkTvIrencFHeOrR3/7htjGxFEnJw6yyiUJtSZVP/bbRcPZ6yJtCMF03nK4IdXsHblyjXXu7u3M+7nrx6KBjew2bOHlUAU52MPOPpyJFADwM66t7P7hxIDJ3Nubwufxukqt+VasJSWI6GN9rtk6Cj1Ro2N2JJ+a4vZSdxl5RrPhujfkh87Vptxncl5G8q7oSjfMXAjk22rsJ+nuYczn57SD5PxYGjO0= mahmmoud.hassanein@gmail.com"

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
COPY rollup.config.js /client_dir

RUN chmod +x /client_dir/start.sh

EXPOSE 8080
ENV HOST=0.0.0.0
ENTRYPOINT ["zinit", "init"]

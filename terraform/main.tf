terraform {
  required_providers {
    grid = {
      source = "threefoldtech/grid"
    #   version = "1.9.3-dev"
    }
  }
}

provider "grid" {
    mnemonics = "actual reveal dish guilt inner film scheme between lonely myself material replace" 
    network = "dev"
}

data "grid_gateway_domain" "server_domain" {
    node = 11
    name = "newcshrserver"
}

data "grid_gateway_domain" "client_domain" {
    node = 11
    name = "newcshr"
}

resource "grid_network" "net2" {
    nodes = [11]
    ip_range = "10.1.0.0/16"
    name = "newcshrnetwork"
    description = "newer network"
    add_wg_access = true
}

resource "grid_deployment" "d1" {
    node = 11
    network_name = grid_network.net2.name
    vms {
        name = "cshrservervm"
        flist = "https://hub.grid.tf/omda.3bot/codescalersinternship-cshr_server-latest.flist"
        cpu = 2 
        memory = 4096
        publicip = false
        planetary = true
        entrypoint = "/sbin/zinit init"
        env_vars = {
            SSH_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCF3JezThwSchTvkF2oPtn8X6chevNsfE58dIY3/eg5zK9tKgNYIB2saoFh12a0AJU424sAeLO0HghhNhe/Co62xkzHhk6EpXWNSFkrlzw+FVn1FKDZbbOZH47sC3n6p5a3YhM4dALssZ/aZdpaKBgXkzk91usJ+GVa+eOnpMRBlHgi9PpvowyzPSKeH9ZcVRBPnVU+nQGyV+kd6RahNBoNgNrHu/QFI92yg/y/7Szus1IS0U92cWKf/K/Sot7O10kSjmj06lMGOO8zdENk/xrtUtRHzemCj+mq0Q/3KUMCGvdb/tH0TDeNenxvibummiym4VTcnYqbm+RDXWG8HUc/RPfEVBl8p1NGZnkBt6QJl5hddHaYwx8CCmf3maSrQFcmrWYtlUDBXYkPyrv0qmy2gM1PScntF/X9zhIfnELlyAVAKXfzVwixrBh7oOIAqefydSVcwWtCXoH38F5q/zo9bQv+eHntI83mZrUUT7JGirQF64fpJKbCZPhv0kUm9bF7DVQMiyRZdk748cgVp7dEzMVlrfZ2eIvZag5zmuJTPB7bw00+Ik9jNaOIhEoCWEaYBw7KmrLonesV8rWUkEAwWPe28bXCVmUZlgZbWJi7BFWCst2Z/j2WgScHbdAv28gAcneDW4yQmt2YaYqXqmwgSVCaD/irq5FSO4upmo5u0Q== mahmmoud.hassanein@gmail.com"
            DJANGO_DEBUG="ON"
            EMAIL="codescalersinternship@gmail.com"
            EMAIL_PASSWORD="ubunyyzgxeoxhnze"
            EMAIL_HOST="smtp.gmail.com"
            REDIS_HOST="redis://localhost:6379"
            DJANGO_SUPERUSER_EMAIL="admin@gmail.com"
            DJANGO_SUPERUSER_PASSWORD="0000"
            SERVER_DOMAIN_NAME=format(data.grid_gateway_domain.server_domain.fqdn)
            CLIENT_DOMAIN_NAME=format(data.grid_gateway_domain.client_domain.fqdn)
        }
    }
}

resource "grid_deployment" "d2" {
    node = 11
    network_name = grid_network.net2.name
    vms {
        name = "cshrclientvmnew"
        publicip = false
        planetary = true
        flist = "https://hub.grid.tf/omda.3bot/codescalersinternship-cshr_client-latest.flist"
        cpu = 2
        memory = 4096
        entrypoint = "/sbin/zinit init"
        env_vars = {
            SSH_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCF3JezThwSchTvkF2oPtn8X6chevNsfE58dIY3/eg5zK9tKgNYIB2saoFh12a0AJU424sAeLO0HghhNhe/Co62xkzHhk6EpXWNSFkrlzw+FVn1FKDZbbOZH47sC3n6p5a3YhM4dALssZ/aZdpaKBgXkzk91usJ+GVa+eOnpMRBlHgi9PpvowyzPSKeH9ZcVRBPnVU+nQGyV+kd6RahNBoNgNrHu/QFI92yg/y/7Szus1IS0U92cWKf/K/Sot7O10kSjmj06lMGOO8zdENk/xrtUtRHzemCj+mq0Q/3KUMCGvdb/tH0TDeNenxvibummiym4VTcnYqbm+RDXWG8HUc/RPfEVBl8p1NGZnkBt6QJl5hddHaYwx8CCmf3maSrQFcmrWYtlUDBXYkPyrv0qmy2gM1PScntF/X9zhIfnELlyAVAKXfzVwixrBh7oOIAqefydSVcwWtCXoH38F5q/zo9bQv+eHntI83mZrUUT7JGirQF64fpJKbCZPhv0kUm9bF7DVQMiyRZdk748cgVp7dEzMVlrfZ2eIvZag5zmuJTPB7bw00+Ik9jNaOIhEoCWEaYBw7KmrLonesV8rWUkEAwWPe28bXCVmUZlgZbWJi7BFWCst2Z/j2WgScHbdAv28gAcneDW4yQmt2YaYqXqmwgSVCaD/irq5FSO4upmo5u0Q== mahmmoud.hassanein@gmail.com"
            SERVER_BASE_URL=format("https://%s", data.grid_gateway_domain.server_domain.fqdn)
        }
    }
}

resource "grid_name_proxy" "p1" {
    node = 11
    name = "newcshrserver"
    backends = [format("http://[%s]:8000", grid_deployment.d1.vms[0].ygg_ip)]
    tls_passthrough = false
}

resource "grid_name_proxy" "p2" {
    node = 11
    name = "newcshr"
    backends = [format("http://[%s]:6000", grid_deployment.d2.vms[0].ygg_ip)]
    tls_passthrough = false
}

output "server_domain" {
    value = data.grid_gateway_domain.server_domain.fqdn
}

output "client_domain" {
    value = data.grid_gateway_domain.client_domain.fqdn
}

output "server_ygg_ip" {
    value = grid_deployment.d1.vms[0].ygg_ip
}

output "client_ygg_ip" {
    value = grid_deployment.d2.vms[0].ygg_ip
}
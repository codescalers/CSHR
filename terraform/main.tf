terraform {
  required_providers {
    grid = {
      source = "threefoldtech/grid"
    #   version = "1.9.3-dev"
    }
  }
}

provider "grid" {
    mnemonics = "" 
    network = ""
}

data "grid_gateway_domain" "server_domain" {
    node = 2
    name = "cshrserver"
}

data "grid_gateway_domain" "client_domain" {
    node = 2
    name = "cshr"
}

resource "grid_network" "net2" {
    nodes = [2]
    ip_range = "10.1.0.0/16"
    name = "newcshrnetwork"
    description = "newer network"
    add_wg_access = true
}

resource "grid_deployment" "d1" {
    node = 2
    network_name = grid_network.net2.name
    vms {
        name = ""
        flist = ""
        cpu = 2 
        memory = 4096
        publicip = false
        planetary = true
        entrypoint = "/sbin/zinit init"
        env_vars = {
            SSH_KEY=""
            DJANGO_DEBUG=""
            EMAIL=""
            EMAIL_PASSWORD=""
            EMAIL_HOST=""
            REDIS_HOST=""
            DJANGO_SUPERUSER_EMAIL=""
            DJANGO_SUPERUSER_PASSWORD=""
            SERVER_DOMAIN_NAME=format(data.grid_gateway_domain.server_domain.fqdn)
            CLIENT_DOMAIN_NAME=format(data.grid_gateway_domain.client_domain.fqdn)
        }
    }
}

resource "grid_deployment" "d2" {
    node = 2
    network_name = grid_network.net2.name
    vms {
        name = "cshrclientvmnew"
        publicip = false
        planetary = true
        flist = ""
        cpu = 2
        memory = 4096
        entrypoint = "/sbin/zinit init"
        env_vars = {
            SSH_KEY = ""
            SERVER_BASE_URL=format("https://%s", data.grid_gateway_domain.server_domain.fqdn)
        }
    }
}

resource "grid_name_proxy" "p1" {
    node = 2
    name = "newcshrserver"
    backends = [format("http://[%s]:8000", grid_deployment.d1.vms[0].ygg_ip)]
    tls_passthrough = false
}

resource "grid_name_proxy" "p2" {
    node = 2
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
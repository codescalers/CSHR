terraform {
  required_providers {
    grid = {
      source = "threefoldtech/grid"
    }
  }
}

provider "grid" {
    mnemonics = "actual reveal dish guilt inner film scheme between lonely myself material replace" 
    network = "dev"
}

data "grid_gateway_domain" "server_domain" {
    node = 14
    name = "cshrserver"
}

data "grid_gateway_domain" "client_domain" {
    node = 14
    name = "cshr"
}

resource "grid_network" "net1" {
    nodes = [14]
    ip_range = "10.1.0.0/16"
    name = "network"
    description = "newer network"
    add_wg_access = true
}

resource "grid_deployment" "d1" {
    node = 14
    network_name = grid_network.net1.name
    vms {
        name = "serverVM"
        flist = "https://hub.grid.tf/omda.3bot/codescalersinternship-cshr_server-latest.flist"
        cpu = 2 
        memory = 1024
        publicip = false
        planetary = true
        entrypoint = "/sbin/zinit init"
        env_vars = {
            SSH_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC8KhnjC8yi2Td7gMEiVmJfUNg1lXE457S+eW1jip0HW3MGLsKjXekauLbR7qcSOKUGURZlsw2KbRdOZnWbQovs24YdevUos/9XIHxFL+mJEy+5gyHuU5Z/yGcuW7O6Qj5xtwvBwe/kWnMtgEd2xXxQqEY3ZHkVh++mA/eqbhikMIsM7Qi5SKBT210+7KT5989BbUpk9e43koFNkVPCXgDR5+frhbEvCq06OVAE8vuEQ/C6EW1ZKn65nVt2z0kA7c8rUE0sEZRnI35oCEwazMlxiPm9B67GryoO7bkTvIrencFHeOrR3/7htjGxFEnJw6yyiUJtSZVP/bbRcPZ6yJtCMF03nK4IdXsHblyjXXu7u3M+7nrx6KBjew2bOHlUAU52MPOPpyJFADwM66t7P7hxIDJ3Nubwufxukqt+VasJSWI6GN9rtk6Cj1Ro2N2JJ+a4vZSdxl5RrPhujfkh87Vptxncl5G8q7oSjfMXAjk22rsJ+nuYczn57SD5PxYGjO0= mahmmoud.hassanein@gmail.com"
            DJANGO_DEBUG="ON"
            EMAIL="codescalersinternship@gmail.com"
            EMAIL_PASSWORD="ubunyyzgxeoxhnze"
            EMAIL_HOST="smtp.gmail.com"
            REDIS_HOST=format("redis://%s:6379", data.grid_gateway_domain.server_domain.fqdn)
            DJANGO_SUPERUSER_EMAIL="admin@gmail.com"
            DJANGO_SUPERUSER_PASSWORD="0000"
            SERVER_DOMAIN_NAME=format(data.grid_gateway_domain.server_domain.fqdn)
            CLIENT_DOMAIN_NAME=format(data.grid_gateway_domain.client_domain.fqdn)
        }
    }
}

resource "grid_deployment" "d2" {
    node = 14
    network_name = grid_network.net1.name
    vms {
        name = "clientVM"
        publicip = false
        planetary = true
        flist = "https://hub.grid.tf/omda.3bot/codescalersinternship-cshr_client-latest.flist"
        cpu = 1
        memory = 1024
        entrypoint = "/sbin/zinit init"
        env_vars = {
            SSH_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC8KhnjC8yi2Td7gMEiVmJfUNg1lXE457S+eW1jip0HW3MGLsKjXekauLbR7qcSOKUGURZlsw2KbRdOZnWbQovs24YdevUos/9XIHxFL+mJEy+5gyHuU5Z/yGcuW7O6Qj5xtwvBwe/kWnMtgEd2xXxQqEY3ZHkVh++mA/eqbhikMIsM7Qi5SKBT210+7KT5989BbUpk9e43koFNkVPCXgDR5+frhbEvCq06OVAE8vuEQ/C6EW1ZKn65nVt2z0kA7c8rUE0sEZRnI35oCEwazMlxiPm9B67GryoO7bkTvIrencFHeOrR3/7htjGxFEnJw6yyiUJtSZVP/bbRcPZ6yJtCMF03nK4IdXsHblyjXXu7u3M+7nrx6KBjew2bOHlUAU52MPOPpyJFADwM66t7P7hxIDJ3Nubwufxukqt+VasJSWI6GN9rtk6Cj1Ro2N2JJ+a4vZSdxl5RrPhujfkh87Vptxncl5G8q7oSjfMXAjk22rsJ+nuYczn57SD5PxYGjO0= mahmmoud.hassanein@gmail.com"
            SERVER_BASE_URL=format("https://%s", data.grid_gateway_domain.server_domain.fqdn)
        }
    }
}

resource "grid_name_proxy" "p1" {
    node = 14
    name = "cshrserver"
    backends = [format("http://[%s]:8000", grid_deployment.d1.vms[0].ygg_ip)]
    tls_passthrough = false
}

resource "grid_name_proxy" "p2" {
    node = 14
    name = "cshr"
    backends = [format("http://[%s]:6000", grid_deployment.d2.vms[0].ygg_ip)]
    tls_passthrough = false
}


# output "publicip_1" {
#     value = grid_deployment.d1.vms[0].computedip
# }

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
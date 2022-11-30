terraform {
  required_providers {
    grid = {
      source = "threefoldtech/grid"
    }
  }
}

provider "grid" {
    mnemonics = "actual reveal dish guilt inner film scheme between lonely myself material replace" 
    network = "qa"
}

data "grid_gateway_domain" "domain" {
    node = 2
    name = "cshr"
}

resource "grid_network" "net1" {
    nodes = [2]
    ip_range = "10.1.0.0/16"
    name = "network"
    description = "newer network"
    add_wg_access = true
}

resource "grid_deployment" "d1" {
    node = 2
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
            DJANGO_SECRET_KEY="tSHKyMyXRsgfliCvjnAzySi5WI8j5f1gJSfxY7UruSq3dE814v"
            DJANGO_DEBUG="ON"
            EMAIL="codescalersinternship@gmail.com"
            EMAIL_PASSWORD="y l g l q y n b m b c s s s z y"
            EMAIL_HOST="smtp.gmail.com"
            REDIS_HOST="redis://localhost:6379"
            DJANGO_SUPERUSER_EMAIL="admin@gmail.com"
            DJANGO_SUPERUSER_PASSWORD="0000"
            SERVER_DOMAIN_NAME=format("https://%s", data.grid_gateway_domain.domain.fqdn)
            CLIENT_DOMAIN_NAME=format("https://%s", data.grid_gateway_domain.domain.fqdn)
        }
    }
}

resource "grid_name_proxy" "p1" {
    node = 2
    name = "cshr"
    backends = [format("http://[%s]:8000", grid_deployment.d1.vms[0].ygg_ip)]
    tls_passthrough = false
}

# resource "grid_deployment" "d2" {
#   node = 14
#   network_name = grid_network.net1.name
#   ip_range = lookup(grid_network.net1.nodes_ip_range, 14, "")
#     vms {
#         name = "clientVM"
#         publicip = true
#         flist = "https://hub.grid.tf/omda.3bot/codescalersinternship-cshr_client-latest.flist"
#         cpu = 1
#         memory = 1024
#         entrypoint = "/sbin/zinit init"
#         env_vars = {
#             SSH_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC8KhnjC8yi2Td7gMEiVmJfUNg1lXE457S+eW1jip0HW3MGLsKjXekauLbR7qcSOKUGURZlsw2KbRdOZnWbQovs24YdevUos/9XIHxFL+mJEy+5gyHuU5Z/yGcuW7O6Qj5xtwvBwe/kWnMtgEd2xXxQqEY3ZHkVh++mA/eqbhikMIsM7Qi5SKBT210+7KT5989BbUpk9e43koFNkVPCXgDR5+frhbEvCq06OVAE8vuEQ/C6EW1ZKn65nVt2z0kA7c8rUE0sEZRnI35oCEwazMlxiPm9B67GryoO7bkTvIrencFHeOrR3/7htjGxFEnJw6yyiUJtSZVP/bbRcPZ6yJtCMF03nK4IdXsHblyjXXu7u3M+7nrx6KBjew2bOHlUAU52MPOPpyJFADwM66t7P7hxIDJ3Nubwufxukqt+VasJSWI6GN9rtk6Cj1Ro2N2JJ+a4vZSdxl5RrPhujfkh87Vptxncl5G8q7oSjfMXAjk22rsJ+nuYczn57SD5PxYGjO0= mahmmoud.hassanein@gmail.com"
#         }
#     }
# }


# output "publicip_1" {
#     value = grid_deployment.d1.vms[0].computedip
# }

output "fqdn" {
    value = data.grid_gateway_domain.domain.fqdn
}
output "ygg_ip" {
    value = grid_deployment.d1.vms[0].ygg_ip
}
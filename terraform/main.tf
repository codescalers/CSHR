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

resource "grid_network" "net1" {
    nodes = [28]
    ip_range = "10.1.0.0/16"
    name = "network"
    description = "newer network"
    add_wg_access = true
}

resource "grid_deployment" "d1" {
  node = 28
  network_name = grid_network.net1.name
  ip_range = lookup(grid_network.net1.nodes_ip_range, 28, "")
    vms {
        name = "serverVM"
        flist = "https://hub.grid.tf/omda.3bot/codescalersinternship-cshr_server-latest.flist"
        cpu = 2 
        memory = 1024
        entrypoint = "/server/start.sh"
        env_vars = {
            SSH_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCvb7z9QW7P7+gJVy8sw3IaJtVdIWPpnhU05NlTcxyRKt74UrOEJ9Ip/wjLsBg4fMZ5voPb9lToMiQ/eV1SqYulDUFSduyfCGucpu+FSvoyKYIgdIoTNIxSZeVm8btvwuO+4UXhpkOzUQ9NZW3SYJcr2rGHlT08jNu0goB9CrhzmGXAKze8+MInENFk4p8PD9ppKn14Fvkded4sMue2GQnKOOXTGy3TWrvyUYrcdLivH2UIiSp4n4/KnINSzwPAz3bNYtaRAkpPDV6vnTQSCi50mL+4bxIzyg51QeDwIRL7EigjRSDRsLkz4yiJ7mk6X5ci/IZTPhHpzVErunOWNwVleCeigB3kt2qUdYBGF+Ev1dVfIq5F+yfdxLlhHvzazx7biPMljqk+sDg0iGcv1gKHGM/+bIPvW+wLMkCLzAVcnDo8+6/V4L6yWZOS39R80fMpfntId9IPiFc1tlc2Fip4B5N0qATKd9C16AU2U4KkKQeMqKCqvhwm05dxB9jmNpfEgA9lWi5m5mdj0YMV0Hqp9YiQmqJ7yQS4JSHVJ0izIWBBOGPVnN/PFggeS8kUbueb9xizhDDO37T/COYLXVCvA7gbAgQ+ACi5bzYDOy83v2KBggfiGuBxmn1KhlX8X1swmCBXTVDLVogwn1KMBLuz9d3fTi6hAE2NTxpzVODa2Q== mahmmoud.hassanein@gmail.com"
        }
        planetary = true
    }
    vms {
        name = "clientVM"
        flist = "https://hub.grid.tf/omda.3bot/codescalersinternship-cshr_client-latest.flist"
        cpu = 1
        memory = 1024
        entrypoint = "/client/start.sh"
        env_vars = {
            SSH_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCvb7z9QW7P7+gJVy8sw3IaJtVdIWPpnhU05NlTcxyRKt74UrOEJ9Ip/wjLsBg4fMZ5voPb9lToMiQ/eV1SqYulDUFSduyfCGucpu+FSvoyKYIgdIoTNIxSZeVm8btvwuO+4UXhpkOzUQ9NZW3SYJcr2rGHlT08jNu0goB9CrhzmGXAKze8+MInENFk4p8PD9ppKn14Fvkded4sMue2GQnKOOXTGy3TWrvyUYrcdLivH2UIiSp4n4/KnINSzwPAz3bNYtaRAkpPDV6vnTQSCi50mL+4bxIzyg51QeDwIRL7EigjRSDRsLkz4yiJ7mk6X5ci/IZTPhHpzVErunOWNwVleCeigB3kt2qUdYBGF+Ev1dVfIq5F+yfdxLlhHvzazx7biPMljqk+sDg0iGcv1gKHGM/+bIPvW+wLMkCLzAVcnDo8+6/V4L6yWZOS39R80fMpfntId9IPiFc1tlc2Fip4B5N0qATKd9C16AU2U4KkKQeMqKCqvhwm05dxB9jmNpfEgA9lWi5m5mdj0YMV0Hqp9YiQmqJ7yQS4JSHVJ0izIWBBOGPVnN/PFggeS8kUbueb9xizhDDO37T/COYLXVCvA7gbAgQ+ACi5bzYDOy83v2KBggfiGuBxmn1KhlX8X1swmCBXTVDLVogwn1KMBLuz9d3fTi6hAE2NTxpzVODa2Q== mahmmoud.hassanein@gmail.com"
        }
        planetary = true
    }
}


output "ygg_ip_1" {
    value = grid_deployment.d1.vms[0].ygg_ip
}
output "ygg_ip_2" {
    value = grid_deployment.d1.vms[1].ygg_ip
}
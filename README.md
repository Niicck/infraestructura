# Infraestructura

This contains the instructions to set up a bare VPS server with everything I need to host my projects.

- [Getting Started](#getting-started)
- [Build a Hetzner Server](#build-a-hetzner-server)
- [Using Hetzner DNS](#using-hetzner-dns)
- [Read more](#read-more)


## Getting Started
1. run `sh utils/install_mac.sh` to install initial ansible dependencies.


## Build a Hetzner Server
1. Create a new project within Hetzer Cloud.
2. Generate a new API token for that project.
3. Add that API token to your `.env` file
4. Create a playbook following the example of `build_supergood_dokku_server.yml`
5. Run your playbook with `source .env && ansible-playbook playbooks/[your-playbook].yml`

## Using Hetzner DNS
1. Create a Hetzner DNS API token at https://dns.hetzner.com/settings/api-token
2. Add that token to `.env` file.

## Read more
- [Hetzner CLI documentation](https://docs.hetzner.cloud/#overview)
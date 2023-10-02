# Infraestructura

This repo contains ansible playbooks for building the server that runs supergood.site.

It will:

- Provision staging and production servers on Hetzner.
- Install basic packages and security configurations on those server.
- Install dokku on those servers.
- Install dokku plugins required for my projects.

And then I have a dokku environment that I can deploy my projects' docker containers on!

Use this repo as a guide for how you might want to deploy your own projects using ansible. You can use it wholesale, but it might be better if you cut/paste/modify it to suit your own needs. You want to deploy on Digitial Ocean instead? You want a third deployment environment? Different databases or plugins? Go for it.

- [Setup](#setup)
  - [1. Install Dependencies](#1-install-dependencies)
  - [2. Configure Vars and Secrets](#2-configure-vars-and-secrets)
  - [3. Setup Hetzner](#3-setup-hetzner)
    - [I want this project to build Hetzner servers for me](#i-want-this-project-to-build-hetzner-servers-for-me)
    - [I want to use my own pre-existing servers](#i-want-to-use-my-own-pre-existing-servers)
  - [4. Setup Cloudflare](#4-setup-cloudflare)
- [Run](#run)

## Setup

### 1. Install Dependencies

First, install ansible if you haven't already.

The project requires some additional ansible collections and python packages to be installed. Install those with:

```bash
make install
```

The Hetzner collection also has some additional python requirements. It's up to you how you want to install them ([venv](https://docs.python.org/3/library/venv.html), [Execution Environments](https://docs.ansible.com/ansible/devel/getting_started_ee/introduction.html), etc.). But installing them on the system is probably fine:

```bash
pip install -r requirements.txt
```

### 2. Configure Vars and Secrets

Install default secrets templates: 

```bash
make secrets
```

Change the vars within group_vars to suit your own project. The current values are what that I'm using to deploy supergood.site. To deploy your own site, at the very least, you'll want to change the `site_domain` and `hetzner.ssh_key_name` within `group_vars/all/main.yml`.

My default hetzner configs will build the cheapest servers available in the US.

### 3. Setup Hetzner

You'll need a server to deploy your dokku project on. This project has a playbook for automatically provisioning Hetzner servers for you. The assumption is that you'll be following that script, but there are suggestions for those who would rather use their own existing servers.

#### I want this project to build Hetzner servers for me

There are a couple manual steps you'll need to take first.

1. Create a new project within Hetzner Cloud.
2. Generate a new API token for that project.
3. Add that API token to `.env` as `HCLOUD_TOKEN`.

After that, the playbooks will have everything it needs to automatically provision Hetzner servers for you.

#### I want to use my own pre-existing servers

If you want to use pre-existing servers instead of building them automatically with `build_hetzner_server.yml` then you'll need to make some manual adjustments to this project.

The simplest way might be to rewrite this project's inventory files to use hardcoded server addresses. Follow the official docs to get an idea of how to do this: https://docs.ansible.com/ansible/latest/getting_started/get_started_inventory.html.

However, if your servers were built on Hetzner you could still use this project's dynamic Hetzner inventory and it will probably work:

1. Add the `HCLOUD_TOKEN` api_token from your pre-existing project to your `.env`.
2. Add the name of your pre-existing servers as `hetzner.server_name` in `group_vars/staging/main.yml` and `group_vars/production/main.yml`.

### 4. Setup Cloudflare

First, you need a domain. If you don't have one already, you can purchase one from a domain name registrar such as [NameCheap](https://www.namecheap.com/).

Once you have a domain, you'll need to point it to the IP address of Hetzner server that you're going to create.

Example:
example.com > 93.184.216.34

This project utilizes Cloudflare as its DNS hosting service to manage these mappings.

The `build_supergood_server.yml` will create records for all subdomains (\*.example.com) as well as create records for all test non-production environments (\*.staging.example.com).

To use Cloudflare:

1. Create a free Cloudflare account
2. Create an API token that has permission to edit any DNS zone.
3. Add that API token to `.env` as `CLOUDFLARE_TOKEN`.

With that API token in place, the `build_supergood_server.yml` playbook will be able to create DNS records for your new server.

## Run

After you've finished setup, you can build your own Hetzner servers by running this playbook:

```bash
./ansible-playbook.sh playbooks/build_supergood_server.yml -e "env=staging"
```

`env=staging` to build the staging environment. `env=production` to build the production environment.

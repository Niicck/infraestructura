#!/bin/bash

pip install ansible
pip install hcloud
ansible-galaxy install dokku_bot.ansible_dokku
ansible-galaxy collection install hetzner.hcloud
ansible-galaxy collection install community.dns.hetzner_dns_records

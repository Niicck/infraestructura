#!/bin/bash

# ! wip, not complete

# Install ansible
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt-get update
sudo apt-get install -y ansible git

# Clone infraestructura repo
git clone git@example.git:main/ansible /tmp/ansible

# Install dokku
pushd /tmp/ansible/ansible > /dev/null
ansible-playbook -s dokku.yml
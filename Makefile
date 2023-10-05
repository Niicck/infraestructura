-include .env
export

# ---------------------
# Setup
# ---------------------

# Install ansible requirements
.PHONY: install
install:
	ansible-galaxy install -r requirements.yml

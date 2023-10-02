-include .env
export

# ---------------------
# Setup
# ---------------------

build_file_from_example = if [ ! -e $(1) ]; then cp $(1).example $(1); echo "Created $(1)"; else echo "Skipping $(1)"; fi

# Create secrets.yml and .env files from example templates, if they don't already exist.
ENVIRONMENTS = staging production
.PHONY: secrets
secrets:
	@for env in $(ENVIRONMENTS); do \
		$(call build_file_from_example, ./group_vars/$$env/secrets.yml); \
	done
	@$(call build_file_from_example, ./host_vars/localhost/secrets.yml)
	@$(call build_file_from_example, ./.env)

# Install ansible requirements
.PHONY: install
install:
	ansible-galaxy install -r requirements.yml

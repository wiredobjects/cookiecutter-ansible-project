.PHONY: terraform virtualenv galaxy test run clean

PLATFORM                   := $(shell uname -s | tr '[:upper:]' '[:lower:]')
ARCHITECTURE               := $(shell uname -m | sed -e 's/x86_64/amd64/')
PROJECT_DIR                 = $(PWD)
DEPLOYMENT_ENV             ?= {{ cookiecutter.deployment_env_dev }}
VENV_ACTIVATE               = source virtualenv/bin/activate
{% if cookiecutter.iaas_use_terraform == 'y' -%}
TERRAFORM_RELEASE          ?= {{ cookiecutter.terraform_release }}
TERRAFORM_RELEASE_ARCHIVE   = terraform_$(TERRAFORM_RELEASE)_$(PLATFORM)_$(ARCHITECTURE)
{% endif -%}
ANSIBLE_DIR_ROLES_EXTERNAL  = roles/external
ANSIBLE_INVENTORY_FILE      = inventory/$(DEPLOYMENT_ENV)
ANSIBLE_EXTRA_VARS          = vars/$(DEPLOYMENT_ENV).yml
ANSIBLE_PLAYBOOK_CMD        = ansible-playbook -i $(ANSIBLE_INVENTORY_FILE) -e "project_dir=$(PWD) -e "@$(ANSIBLE_EXTRA_VARS)"

{% if cookiecutter.iaas_use_terraform == 'y' -%}
get-terraform: bin/terraform
{% endif -%}
virtualenv: virtualenv/.built
galaxy: roles/external/.built

help:
	@echo 'Usage:'
	{% if cookiecutter.iaas_use_terraform == 'y' -%}
	@echo '    make get-terraform   Fetch Terraform release $(TERRAFORM_RELEASE) from HashiCorp'
	{% endif -%}
	@echo '    make virtualenv      Prepare the virtualenv environment'
	@echo '    make galaxy          Download external roles from galaxy or custom sources'
	@echo '    make test            Ansible playbooks tests'
	{% if cookiecutter.iaas_role_enable -%}
	@echo '    make run-iaas        Ansible/Terraform run for IaaS'
	{% endif -%}
	@echo '    make run             Ansible playbook run'
	@echo '    make clean           Remove virtualenv environment and external galaxy roles'
	@echo '    make all             Run: virtualenv galaxy test run'
	@echo

all: virtualenv galaxy test run

{% if cookiecutter.iaas_use_terraform == 'y' -%}
bin/terraform:
	curl -O https://releases.hashicorp.com/terraform/$(TERRAFORM_RELEASE)/$(TERRAFORM_RELEASE_ARCHIVE).zip
	unzip $(TERRAFORM_RELEASE_ARCHIVE) -d bin
	rm -f $(TERRAFORM_RELEASE_ARCHIVE).zip
{% endif -%}

virtualenv/.built: requirements.txt
	rm -rf virtualenv
	virtualenv virtualenv
	$(VENV_ACTIVATE) && pip install -r requirements.txt
	touch $@

roles/external/.built: virtualenv/.built roles/requirements.yml
	$(VENV_ACTIVATE) && ansible-galaxy install -r roles/requirements.yml -p $(ANSIBLE_DIR_ROLES_EXTERNAL)
	touch $@

test:
	$(VENV_ACTIVATE) && $(ANSIBLE_PLAYBOOK_CMD) --syntax-check site.yml
	$(VENV_ACTIVATE) && ansible-lint --exclude $(ANSIBLE_DIR_ROLES_EXTERNAL) site.yml

{% if cookiecutter.iaas_role_enable -%}
run-iaas:
	mkdir -p build/terraform/$(DEPLOYMENT_ENV)
	mkdir -p terraform_states/$(DEPLOYMENT_ENV)
	$(VENV_ACTIVATE) && $(ANSIBLE_PLAYBOOK_CMD) iaas.yml
	terraform apply -state terraform_states/$(DEPLOYMENT_ENV)/terraform.tfstate build/terraform/$(DEPLOYMENT_ENV)
{% endif -%}

run: {% if cookiecutter.iaas_role_enable %} run-iaas {% endif %}
	$(VENV_ACTIVATE) && $(ANSIBLE_PLAYBOOK_CMD) site.yml

clean:
	rm -rf bin/terraform
	rm -rf virtualenv
	rm -rf $(ANSIBLE_DIR_ROLES_EXTERNAL)/*
	rm -rf site.retry

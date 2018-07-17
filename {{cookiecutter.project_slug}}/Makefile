.PHONY: virtualenv galaxy test run clean

PROJECT_DIR                 = $(PWD)
DEPLOYMENT_ENV             ?= {{ cookiecutter.deployment_env_dev }}
VENV_ACTIVATE               = source virtualenv/bin/activate
ANSIBLE_DIR_ROLES_EXTERNAL  = roles/external
ANSIBLE_INVENTORY_FILE      = inventory/$(DEPLOYMENT_ENV)
ANSIBLE_EXTRA_VARS          = vars/$(DEPLOYMENT_ENV).yml
ANSIBLE_PLAYBOOK_CMD        = ansible-playbook -i $(ANSIBLE_INVENTORY_FILE) -e "project_dir=$(PWD) -e "@$(ANSIBLE_EXTRA_VARS)"

virtualenv: virtualenv/.built
galaxy: roles/external/.built

print_basedir:
	@echo $(PROJECT_BASE_DIR)
help:
	@echo 'Usage:'
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
	rm -rf virtualenv
	rm -rf $(ANSIBLE_DIR_ROLES_EXTERNAL)/*
	rm -rf site.retry

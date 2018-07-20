.PHONY: virtualenv test docs clean

VENV_ACTIVATE           = source virtualenv/bin/activate

virtualenv: virtualenv/.built

help:
	@echo 'Usage:'
	@echo '    make virtualenv         Clean and prepare a new virtualenv'
	@echo '    make test               Test the cookie'
	@echo '    make docs               Render documentation'
	@echo '    make clean              Remove virtualenv environment'
	@echo

virtualenv/.built: requirements.txt
	virtualenv virtualenv
	$(VENV_ACTIVATE) && pip install -r requirements.txt
	touch $@

test:
	$(VENV_ACTIVATE) && tox -e py27

docs:
	$(VENV_ACTIVATE) && $(MAKE) -C docs clean html

clean:
	$(VENV_ACTIVATE) && $(MAKE) -C docs clean 
	rm -rf virtualenv


.PHONY: virtualenv test clean

VENV_ACTIVATE           = source virtualenv/bin/activate

virtualenv: virtualenv/.built

help:
	@echo 'Usage:'
	@echo '    make virtualenv         Clean and prepare a new virtualenv'
	@echo '    make test               Test the cookie'
	@echo '    make clean              Remove virtualenv environment'
	@echo

virtualenv/.built: clean requirements.txt
	virtualenv virtualenv
	$(VENV_ACTIVATE) && pip install -r requirements.txt
	touch $@

test:
	$(VENV_ACTIVATE) && tox -e py27

clean:
	rm -rf virtualenv

MAKEFLAGS = --no-print-directory --always-make --silent
MAKE = make $(MAKEFLAGS)

VENV_NAME = flask-skeleton
VENV_PATH = ~/.virtualenvs/$(VENV_NAME)
VENV_ACTIVATE = . $(VENV_PATH)/bin/activate

clean:
	find . -name "*.pyc" -print -delete
	find . \( -name "*.min.js" -o -name "*.min.css" \) -print -delete
	rm -rfv $(VENV_PATH)

check:
	$(MAKE) virtualenv
	$(MAKE) pylint pep8 nosetests

virtualenv:
	test -d $(VENV_PATH) || virtualenv $(VENV_PATH)
	$(VENV_ACTIVATE) && python setup.py --quiet develop

pep8:
	@echo "Running pep8..."
	$(VENV_ACTIVATE) && \
	pep8 src/data && \
	pep8 src/web && \
	pep8 src/tests && \
	pep8 src/*.py

pylint:
	@echo "Running pylint..."
	$(VENV_ACTIVATE) && \
    pylint src/data && \
    pylint src/web && \
    pylint src/tests && \
    pylint src/*.py

nosetests:
	@echo "Running nosetests..."
	$(VENV_ACTIVATE) && nosetests

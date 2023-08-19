export PIPENV_VERBOSITY=-1

.PHONY: install
install: venv
	. venv/bin/activate && pipenv install --dev

.PHONY: venv
venv:
	test -d venv || python3 -m venv venv

.PHONY: lock
lock:
	. venv/bin/activate && pipenv lock

.PHONY: lint
lint:
	. venv/bin/activate && pipenv run flake8

PYTHON ?= python3

.PHONY: install install-dev test run

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

install-dev:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements-dev.txt

test:
	$(PYTHON) -m pytest

run:
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port $${PORT:-8000}

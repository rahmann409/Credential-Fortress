.PHONY: install test lint clean

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

install: $(VENV)/bin/activate
	$(PIP) install -e .[dev]

test: install
	$(PYTHON) -m pytest tests/ --cov=credential_fortress --cov-report=term-missing --cov-fail-under=80

lint: install
	$(PYTHON) -m ruff check .
	$(PYTHON) -m mypy credential_fortress/

clean:
	rm -rf $(VENV)
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -r {} +

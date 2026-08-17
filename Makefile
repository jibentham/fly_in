PYTHON      = .venv/bin/python3
PIP         = .venv/bin/pip
MAIN        = src/main.py
NAME        = fly_in
VERSION     = 1.0.0
TARBALL     = $(NAME)-$(VERSION).tar.gz
INSTALL_DIR = $(NAME)-$(VERSION)
SOURCES     = src/ maps/ .gitignore Makefile README.md fly_in.md
SOURCES_PY  = src/

install:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy
	source .venv/bin/activate
	@echo "Virtual environment created. Run 'make run' to start."

run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) pdb $(MAIN)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -f output.txt

lint:
	.venv/bin/flake8 $(SOURCES_PY)
	.venv/bin/mypy $(SOURCES_PY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	.venv/bin/flake8 $(SOURCES_PY)
	.venv/bin/mypy $(SOURCES_PY) --strict

.PHONY: install run debug clean lint lint-strict

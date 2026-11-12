PYTHON      = python3
VENV        = .venv
VPYTHON     = $(VENV)/bin/python
MAIN        = src/main.py
NAME        = fly_in
VERSION      = 1.0.0
TARBALL     = $(NAME)-$(VERSION).tar.gz
INSTALL_DIR  = $(NAME)-$(VERSION)
SOURCES      = src/ maps/ .gitignore Makefile README.md fly_in.md
SOURCES_PY   = src/

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m venv $(VENV)
	$(VPYTHON) -m pip install --upgrade pip
	$(VPYTHON) -m pip install flake8 mypy pygame-ce matplotlib
	@echo "Virtual environment created. Run 'make run' to start."

run:
	$(VPYTHON) $(MAIN)

debug:
	$(VPYTHON) -m pdb $(MAIN)

clean:
	@echo "Cleaning temporary files and caches..."
	@rm -rf $(VENV) venv dist/ build/
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	@find . -type d -name "*-info" -prune -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete!"

lint:
	$(VENV)/bin/flake8 $(SOURCES_PY)
	$(VENV)/bin/mypy $(SOURCES_PY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(VENV)/bin/flake8 $(SOURCES_PY)
	$(VENV)/bin/mypy $(SOURCES_PY) --strict

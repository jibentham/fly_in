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
	$(PIP) install flake8 mypy pygame
	@echo "Virtual environment created. Run 'make run' to start."

run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) pdb $(MAIN)

clean:
	@echo "Cleaning temporary files and caches..."
	@if [ -d "venv" ]; then rm -rf venv && echo " - Removed venv/"; fi
	@if [ -d ".venv" ]; then rm -rf .venv; fi
	@rm -rf dist/ build/ 2>/dev/null || true
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleanup complete!"


lint:
	.venv/bin/flake8 $(SOURCES_PY)
	.venv/bin/mypy $(SOURCES_PY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	.venv/bin/flake8 $(SOURCES_PY)
	.venv/bin/mypy $(SOURCES_PY) --strict

.PHONY: install run debug clean lint lint-strict

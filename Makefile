# =========================================================
# AnalystStack — developer tasks (Windows / PowerShell)
# =========================================================

SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -ExecutionPolicy Bypass -Command

PYTHON := python

# =========================================================
# Environment
# =========================================================

.PHONY: install
install:
	$(PYTHON) -m pip install -e ".[dev,bigquery]"

# =========================================================
# Quality
# =========================================================

.PHONY: format
format:
	ruff format src/AnalystStack test

.PHONY: lint
lint:
# 	flake8 src/AnalystStack test
	ruff check src/AnalystStack test --fix

.PHONY: typecheck
typecheck:
	mypy --ignore-missing-imports src/AnalystStack test

.PHONY: test
test:
	pytest

.PHONY: check
check: format lint typecheck test

# =========================================================
# Build / docs
# =========================================================

.PHONY: build
build: clean
	$(PYTHON) -m build

.PHONY: docs
docs:
	cd docs; zensical build --clean

.PHONY: docs-serve
docs-serve:
	cd docs; zensical serve

.PHONY: clean
clean:
	Remove-Item -Recurse -Force build, dist, *.egg-info, src/*.egg-info, docs/site, docs/.cache -ErrorAction SilentlyContinue
	Get-ChildItem -Recurse -Include __pycache__, .pytest_cache, .mypy_cache -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

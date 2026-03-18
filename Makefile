# =========================================================
# Bootstrap Makefile
# =========================================================

SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -ExecutionPolicy Bypass -Command

PROJECT_NAME := my_datascience_project
PYTHON := python
VENV := .venv
PYTHON_VENV := venv\Scripts\python.exe

# =========================================================
# Build the package
# =========================================================

.PHONY: build
build:
	Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
	pyproject-build
	py -m pip install .

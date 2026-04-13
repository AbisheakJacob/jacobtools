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

.PHONY: clean
clean:
	Remove-Item -Recurse -Force .tox
	Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
	Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
	Remove-Item -Recurse -Force *.egg-info -ErrorAction SilentlyContinue
	Remove-Item -Recurse -Force .tox -ErrorAction SilentlyContinue

.PHONY: freeze
freeze: 
	pip freeze > requirements.txt

.PHONY: git
git:
	pip freeze > requirements.txt
	git add .
	git commit -m "$(msg)"
	git push

.PHONY: git_recommit
git_recommit:
	pip freeze > requirements.txt
	git add .
	git commit --amend --no-edit
	git push --force

.PHONY: pull
git_pull:
	git pull
	pip install -r requirements.txt

.PHONY: build
build:
	Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
	pyproject-build
	py -m pip install .
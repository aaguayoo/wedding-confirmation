#######################################
##### Makefile for Python-Project #####
#######################################

##################
## Set PROJET_PATH
##################
PROJECT_PATH=${PWD}

#################
## Default target
#################
.DEFAULT_GOAL := help

#######
## Init
#######
.PHONY: install
install: start-message project-info poetry-dev  ## Initialize repo and install dependencies. &&  make install

start-message:
	@echo ""
	@echo "\033[1;39m#####################################\033[0m"
	@echo "\033[1;39m######### PYTHON - PROJECT ##########\033[0m" 
	@echo "\033[1;39m#####################################\033[0m"
	@echo ""

project-info:
	@echo "Project: \033[1;33m{{cookiecutter.project_name.title()}}\033[0m"
	@echo "Author: \033[1;33m{{cookiecutter.author}}\033[0m"
	@echo "Email: \033[1;33m{{cookiecutter.email}}\033[0m"
	@echo "Description: \033[1;33m{{cookiecutter.description}}\033[0m"
	@echo ""

######
## API
######
.PHONY: api
api: start-message  ## Deploy API. &&  make api
	@echo "\033[0;35m#######################\033[0m"
	@echo "\033[0;35m##  RUN PROJECT API  ##\033[0m"
	@echo "\033[0;35m#######################\033[0m"
	@echo "Running uvicorn"
	@echo "Swagger UI available at: \033[1;33mhttp://127.0.0.1:8100/docs\033[0m"
	@poetry run uvicorn app.main:app --host 127.0.0.1 --port 8100 --reload --log-level info
	@echo ""

#################
## Change version
#################
change-version: start-message  ## Change project version. &&  make change-version version=X.X.X
	@echo "\033[0;35m######################\033[0m"
	@echo "\033[0;35m##  CHANGE VERSION  ##\033[0m"
	@echo "\033[0;35m######################\033[0m"
ifdef version
	@old_version=$(shell cat pyproject.toml | awk '/^version =/{print $$3}' | xargs); \
	echo "Changing from version v$$old_version to v${version}..."; \
	cat pyproject.toml | awk '/^version =/{gsub($$3,"\"${version}\"")};{print}' > temp && mv temp pyproject.toml; \
	cat docs/design_doc.md | awk '/- Version:/{gsub($$3,"${version}")};{print}' > temp && mv temp docs/design_doc.md; \
	cat docs/index.md | awk '/Version:/{gsub($$3,"${version}")};{print}' > temp && mv temp docs/index.md; \
	cat README.md | awk '/Version:/{gsub($$3,"${version}")};{print}' > temp && mv temp README.md; \
	cat app/core/config.py | awk '/    VERSION: str =/{gsub($$3,"\"${version}\"")};{print}' > temp && mv temp app/core/config.py; \
	cat {{cookiecutter.project_slug}}/__init__.py | awk '/^__version__ =/{gsub($$3,"\"${version}\"")};{print}' > temp && mv temp {{cookiecutter.project_slug}}/__init__.py; \
	cat tests/test_{{cookiecutter.project_slug}}.py | awk '/__version__ ==/{gsub($$4,"\"${version}\"")};{print}' > temp && mv temp tests/test_{{cookiecutter.project_slug}}.py
	@echo ""
	@echo "\033[0;35m##################\033[0m"
	@echo "\033[0;35m##  DOC DEPLOY  ##\033[0m"
	@echo "\033[0;35m##################\033[0m"
	@echo "Deploying documentation for version v${version}"
	@poetry run mike deploy v${version} 
	@poetry run mike set-default v${version}
	@echo ""
else
	@echo "\033[0;31mPlease set the version number:\033[0m \033[1;39m $$ make change-version version=<version_number>\033[0m"
	@echo ""
endif

#########
## Commit
#########
.PHONY: commit
commit: start-message pre-commit  ## Run Git commit using Commitizen. &&  make commit
	@echo "\033[0;35m##################\033[0m"
	@echo "\033[0;35m##  GIT COMMIT  ##\033[0m"
	@echo "\033[0;35m##################\033[0m"
	@echo "Running commitizen CHANGELOG.md update..."
	-poetry run cz changelog
	@git add .
	@echo ""
	@echo "Running comitizen commit..."
	@poetry run pre-commit run
	@poetry run cz commit
	@echo ""

################
## Documentation
################
.PHONY: docs
doc-deploy: start-message  ## Deploy MkDocs documentation in Github Pages. &&  make doc-deploy
	@echo "\033[0;35m##################\033[0m"
	@echo "\033[0;35m##  DOC DEPLOY  ##\033[0m"
	@echo "\033[0;35m##################\033[0m"
ifdef version
	@echo "Deploying documentation for version ${version}"
	@poetry run mike deploy v${version} -b gh-pages --push
	@poetry run mike set-default v${version}
	@echo "Deploying documentation in localhost..."
	@poetry run mike serve
	@echo ""
else
	@version=$(shell cat pyproject.toml | awk '/^version =/{print $$3}' | xargs); \
	echo "Deploying documentation for version $$version"; \
	poetry run mike deploy v$$version -b gh-pages --push; \
	poetry run mike set-default v$$version && echo "\033[0;32mDocumentation deployed successfully.\033[0m" || echo "\033[0;31mAn error has ocurred while deploying documentation\033[0m"
	@echo "Deploying documentation in localhost..."
	@poetry run mike serve
	@echo ""
endif

doc-serve: start-message  ## Deploy MkDocs documentation locally. &&  make doc-serve
	@echo "\033[0;35m#################\033[0m"
	@echo "\033[0;35m##  DOC SERVE  ##\033[0m"
	@echo "\033[0;35m#################\033[0m"
	@echo "Deploying documentation"
	@poetry run mkdocs serve
	@echo ""

#######################
## Jupyter Lab/Notebook
#######################
.PHONY: jupyter
jupyter-lab: start-message  ## Run Jupyter-Lab. &&  make jupyter-lab
	@echo "\033[0;35m###################\033[0m"
	@echo "\033[0;35m##  JUPYTER-LAB  ##\033[0m"
	@echo "\033[0;35m###################\033[0m"
	@echo "Deploying Jupyter-Lab in localhost..."
	@poetry run jupyter-lab
	@echo ""

jupyter-notebook: start-message  ## Run Jupyter-Notebook. &&  make jupyter-notebook
	@echo "\033[0;35m#######################\033[0m"
	@echo "\033[0;35m##  JUPYTER-NOTEBOOK ##\033[0m"
	@echo "\033[0;35m#######################\033[0m"
	@echo "Deploying Jupyter Notebook in localhost..."
	@poetry run jupyter notebook
	@echo ""

#########
## Poetry
#########
.PHONY: poetry
poetry-dev: start-message
	@echo "\033[0;35m#########################\033[0m"
	@echo "\033[0;35m##  POETRY INSTALL DEV ##\033[0m"
	@echo "\033[0;35m#########################\033[0m"
	@echo "Installing dependencies in Poetry environment..."
	@poetry config virtualenvs.path '${PROJECT_PATH}/.venv-dev' --local
	@poetry install
	@poetry export --format=requirements.txt --without-hashes > '${PROJECT_PATH}/requirements/common.txt'
	@poetry install --only dev,doc,api
	@poetry export --only dev --format=requirements.txt --without-hashes > '${PROJECT_PATH}/requirements/dev.txt'
	@poetry export --only doc --format=requirements.txt --without-hashes > '${PROJECT_PATH}/requirements/doc.txt'
	@poetry export --only api --format=requirements.txt --without-hashes > '${PROJECT_PATH}/requirements/api.txt'
	@echo ""
	@echo "Creating dependencies documentation..."
	@poetry run python docs/generate_dependencies_doc.py
	@echo ""
	@echo "\033[0;35m##########################\033[0m"
	@echo "\033[0;35m##  PRE-COMMIT INSTALL  ##\033[0m"
	@echo "\033[0;35m##########################\033[0m"
	@echo "Installing pre-commit..."
	@poetry run pre-commit install
	@echo ""
	@echo "\033[0;35m###################\033[0m"
	@echo "\033[0;35m##  POETRY SHELL ##\033[0m"
	@echo "\033[0;35m###################\033[0m"
	@echo "Entering Poetry environment shell..."
	@poetry shell
	@echo ""

poetry-prod: start-message
	@echo "\033[0;35m##########################\033[0m"
	@echo "\033[0;35m##  POETRY INSTALL PROD ##\033[0m"
	@echo "\033[0;35m##########################\033[0m"
	@echo "Installing dependencies in Poetry environment..."
	@poetry config virtualenvs.path '${PROJECT_PATH}/.venv-prod' --local
	@poetry install
	@poetry export --format=requirements.txt --without-hashes > '${PROJECT_PATH}/requirements/common.txt'
	@poetry install --only prod
	@poetry export --only prod --format=requirements.txt --without-hashes > '${PROJECT_PATH}/requirements/prod.txt'
	@echo ""
	@echo "\033[0;35m###################\033[0m"
	@echo "\033[0;35m##  POETRY SHELL ##\033[0m"
	@echo "\033[0;35m###################\033[0m"
	@echo "Entering Poetry environment shell..."
	@poetry shell
	@echo ""

poetry-remove: start-message  ## Remove Poetry environment. &&  make poetry-remove
	@echo "\033[0;35m#####################\033[0m"
	@echo "\033[0;35m##  POETRY REMOVE  ##\033[0m"
	@echo "\033[0;35m#####################\033[0m"
	@echo "Removing Poetry environment $(shell poetry env list | awk '{print $$1}')..."
	@poetry env remove $(shell poetry env list | awk '{print $$1}')
	@rm -rf .venv*
	@echo "Poetry environment removed."
	@echo ""
	@echo "Removing poetry.lock..."
	@rm poetry.lock
	@echo "Poetry lock removed."
	@echo ""

#############
## Pre-commit
#############
.PHONY: pre-commit
pre-commit: start-message  ## Run Pre-Commit-Hooks. &&  make pre-commit
	@echo "\033[0;35m##################\033[0m"
	@echo "\033[0;35m##  PRE-COMMIT  ##\033[0m"
	@echo "\033[0;35m##################\033[0m"
	@cd '${PROJECT_PATH}/'
	@git add .
	@pre-commit run
	@echo ""

##########
## Profile
##########
.PHONY: profile
profile: start-message  ## Perform package profiling. &&  make profile
	@echo "\033[0;35m############################\033[0m"
	@echo "\033[0;35m##  PERFORMANCE ANALYSIS  ##\033[0m"
	@echo "\033[0;35m############################\033[0m"
	@echo "Running CPU and RAM memory profiling..."
	@poetry run python '${PROJECT_PATH}/profiling/{{cookiecutter.project_slug}}_profiling.py' > profiling/memory_profiler.log && echo "\033[0;32mProfiling log saved in profiling/memory_profiler.log.\033[0m" || echo "\033[0;31mError running performance anlaysis.\033[0m"
	@mv plot.png profiling/memory_profiler_plot.png
	@echo "\033[0;32mMemory and CPU usage reported in profiling/memory_profiler_plot.png.\033[0m"

#############
## Pre-commit
#############
.PHONY: streamlit 
streamlit: start-message  ## Deploy Streamlit demo app locally. &&  make streamlit
	@echo "\033[0;35m#####################\033[0m"
	@echo "\033[0;35m##  STREAMLIT APP  ##\033[0m"
	@echo "\033[0;35m#####################\033[0m"
	@cd '${PROJECT_PATH}/'
	@poetry run streamlit run demo/{{cookiecutter.project_slug}}_demo.py
	@echo ""

##############
## Release Tag
##############
.PHONY: tag
tag: start-message  ## Create a new tag version. &&  make tag version=X.X.X
	@echo "\033[0;35m#################\033[0m"
	@echo "\033[0;35m## TAG-VERSION ##\033[0m"
	@echo "\033[0;35m#################\033[0m"
ifdef version
	@echo "Fixing tag/version v${version} from current commit..." && (git tag -a v${version} -m "git Reponame v${version}" && echo "\033[0;32mTag v${version} created\033[0m" && git push origin v${version}) || (echo "\033[0;31mERROR:\033[0m Listing all existing tags:" && git tag --list)
else
	@version=$(shell cat pyproject.toml | awk '/^version =/{print $$3}' | xargs); \
	echo "Fixing tag/version v$$version from current commit..." && (git tag -a v$$version -m "git Reponame v$$version" && echo "\033[0;32mTag v$$version created\033[0m" && git push origin v$$version) || (echo "\033[0;31mERROR:\033[0m Listing all existing tags:" && git tag --list)
	@echo ""
endif
	
########
## Tests
########
.PHONY: test
test: start-message  ## Run tests using Pytest and Code-Coverage. &&  make test
	@echo "\033[0;35m#############\033[0m"
	@echo "\033[0;35m##  TESTS  ##\033[0m"
	@echo "\033[0;35m#############\033[0m"
	@echo "Running unit tests..."
	@poetry run coverage run -m pytest '${PROJECT_PATH}/tests/'
	@poetry run coverage html -d docs/coverage --omit="*cache*"
	@echo ""

#######
## Help
#######
.PHONY: help
help: start-message ## DEFAULT. Show this help message. &&  make help
	@echo "\033[1;35m####################################################################\033[0m"
	@echo "\033[1;35m##                     MAKEFILE FOR PYTHON - PROJECT              ##\033[0m"
	@echo "\033[1;35m####################################################################\033[0m"
	@echo ""
	@echo "Use as: \033[32mmake <target> <option>=<value>\033[0m"
	@echo ""
	@echo "Targets available:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | awk 'BEGIN {FS = "&&.*?  "}; {printf "%s\n                         \033[33mExample: %s\033[0m\n", $$1, $$2}'
	@echo "   "
	@echo "\033[1;35m####################################################################\033[0m"


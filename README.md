# Trabalho individual de GCES 2022-2
|Aluno|Matrícula|
|--|--|
|João Vitor de Souza Durso|180123459|


| Item | Peso |
|---|---|
| 1. Containerização do Banco                      | 1.0 |
| 2. Containerização da biblioteca + Banco          | 1.5 |
| 3. Publicação da biblioteca  | 1.5 |
| 4. Documentação automatizada | 1.5 |
| 5. Integração Contínua (Build, Test, Lint, Documentação)       | 3.0 |
| 6. Deploy Contínuo                               | 1.5 |


## 1. Containerização do Banco

Criação do [docker-compose.yaml](docker-compose.yaml) com a definição do container do MongoDB.

### docker-compose.yaml
```yaml
version: '3.5'

services:
  postgres:
    image: postgres
    restart: always
    container_name: postgres
    env_file:
      - metabase/config/postgres_exemple.env

  metabase:
    image: metabase/metabase
    ports:
      - 3001:3000
    env_file:
      - metabase/config/metabase_database_exemple.env
    depends_on:
      - postgres
```

Para comprovar o funcionamento, basta executar:

```
sudo docker-compose up --remove-orphans
```
```
docker exec -it $(docker ps -f "name=mongo" -q) mongosh
```
```
use admin
```
```
db.auth('lappis','l4pp1s')
```

## 2. Containerização da biblioteca + Banco

Nessa etapa, criou-se o [Dockerfile](Dockerfile). Depois adicionou-se alterações ao [docker-compose.yaml](docker-compose.yaml) para adicionar a biblioteca quando rodar o Docker.

### docker-compose.yaml
```yaml
version: '3.5'

services:
  postgres:
    image: postgres
    restart: always
    container_name: postgres
    env_file:
      - metabase/config/postgres_exemple.env

  metabase:
    image: metabase/metabase
    ports:
      - 3001:3000
    env_file:
      - metabase/config/metabase_database_exemple.env
    depends_on:
      - postgres

  lib:
    build: .
```

### Dockerfile
```Dockerfile
FROM python:3.8 AS python

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN python -m pip install --upgrade pip \
    pip install poetry

RUN poetry install

RUN apt update -y
RUN apt-get install python3-sphinx -y
RUN apt-get install doxygen sphinx-common -y

RUN doxygen doxygen.conf -y
RUN sphinx-build -b html docs/source docs/build
```

Para ratificar o funcionamento, basta executar:

```
sudo docker-compose up --remove-orphans
```

## 3. Publicação da biblioteca

Nesta etapa, inicializou-se o poetry:

```
poetry init
```

O comando abaixo serve para adicionar todas as dependências do projeto no arquivo [poetry.lock](poetry.lock).
```
poetry add $(cat requirements.txt)
```

O comando abaixo gera a biblioteca das dependências.
```
poetry build
```

Os dois comandos abaixo são para configurar o token do PyPi e publicar a biblioteca no Pypi.
```
poetry config pypi-token.pypi <TOKEN>
```

```
poetry publish --skip-existing
```

Para ratificar o sucesso, acesse o link abaixo para ver a biblioteca publicada:

### Link da Biblioteca Publicada
https://pypi.org/project/trabalho-individual-2022-2-jvsdurso/

Ou utilize o comando:

```
pip3 install https://pypi.org/project/trabalho-individual-2022-2-jvsdurso/
```

## 4. Documentação automatizada

Nesta etapa, inicializou-se o Doxygen e o Sphinx:

Primeiro, é preciso instalar o Doxygen:

Em seguida, gera-se um arquivo [Doxyfile](doxygen.conf), colocando as configurações desejadas.

```
doxygen -g doxygen.conf
```

### doxygen.conf

```
# Doxyfile 1.9.1

# This file describes the settings to be used by the documentation system
# doxygen (www.doxygen.org) for a project.
#
# All text after a double hash (##) is considered a comment and is placed in
# front of the TAG it is preceding.
#
# All text after a single hash (#) is considered a comment and will be ignored.
# The format is:
# TAG = value [value, ...]
# For lists, items can also be appended using:
# TAG += value [value, ...]
# Values that contain spaces should be placed between quotes (\" \").

#---------------------------------------------------------------------------
# Project related configuration options
#---------------------------------------------------------------------------

# The PROJECT_NAME tag is a single word (or a sequence of words surrounded by
# double-quotes, unless you are using Doxywizard) that should identify the
# project for which the documentation is generated. This name is used in the
# title of most generated pages and in a few other places.
# The default value is: My Project.

PROJECT_NAME           = "trabalho-individual-2022-2-jvsdurso"

# The OUTPUT_DIRECTORY tag is used to specify the (relative or absolute) path
# into which the generated documentation will be written. If a relative path is
# entered, it will be relative to the location where doxygen was started. If
# left blank the current directory will be used.

OUTPUT_DIRECTORY       = "doxygen_output"

#---------------------------------------------------------------------------
# Configuration options related to the input files
#---------------------------------------------------------------------------

# The INPUT tag is used to specify the files and/or directories that contain
# documented source files. You may enter file names like myfile.cpp or
# directories like /usr/src/myproject. Separate the files or directories with
# spaces. See also FILE_PATTERNS and EXTENSION_MAPPING
# Note: If this tag is empty the current directory is searched.

INPUT                  = "src"

#---------------------------------------------------------------------------
# Configuration options related to the XML output
#---------------------------------------------------------------------------

# If the GENERATE_XML tag is set to YES, doxygen will generate an XML file that
# captures the structure of the code including all documentation.
# The default value is: NO.

GENERATE_XML           = YES
```

Por fim, gerou-se a documentação em XML executando:

```
doxygen doxygen.conf
```

Em seguida, inicia-se o Sphinx, utilizando os comandos:

```
mkdir docs
cd docs
sphinx-quickstart
```

Adiciona-se as configurações desejadas:

### conf.py
```py
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))


# -- Project information -----------------------------------------------------

project = 'trabalho-individual-2022-2-jvsdurso'
copyright = '2023, João Durso'
author = 'João Durso'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

```

## 5. Integração Contínua (Build, Test, Lint, Documentação)

Para criar a integração contínua, criou-se o arquivo [ci-cd.yml](.github/workflows/ci-cd.yml) que acionará o GitHub Actions a cada atualização da master.

### ci-cd.yml
```yml
name: GCES CI/CD

on:
  push:
    branches:
      - main
    pull_request:
      - main

env:
  ACTIONS_ALLOW_UNSECURE_COMMANDS: "true"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Copy master...
      uses: actions/checkout@v2

    - name: Config python...
      uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: Installing poetry...
      run: python -m pip install poetry

    - name: Installing sphinx...
      run: sudo apt install --allow-unauthenticated python3-sphinx -y

    - name: Check for new Python version...
      run: |
        NEW_VERSION=$(curl --silent https://www.python.org/ftp/python/ | grep -Eo 'python-[0-9\.]+' | sort -V | tail -1)
        INSTALLED_VERSION=$(python3 --version | awk '{print $2}')
        if [ "$NEW_VERSION" != "$INSTALLED_VERSION" ]; then
          echo "Updating Python from $INSTALLED_VERSION to $NEW_VERSION"
          sudo apt-get update
          sudo apt-get install -y $NEW_VERSION
        else
          echo "Python is up-to-date ($INSTALLED_VERSION)"
        fi

    - name: Installing requirements...
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt 

    - name: Watching lint...
      run: |
        pip install pylint
        pylint src
      continue-on-error: true

    - name: Testing...
      run: poetry run pytest --cov 

    - name: Generate documentation...
      run: sphinx-build -b html docs/source docs/build

    - name: Publishing in poetry...
      run: |
        poetry version patch
        poetry build -v
        poetry install
        poetry config pypi-token.pypi ${{ secrets.PYPI_TOKEN }}
        poetry publish ----skip-existing

```

É possível ver o GitHub Actions funcionando no [link](https://github.com/jvsdurso/Trabalho-Individual-2022-2/actions).

## 6. Deploy Contínuo

O deploy contínuo foi feito no mesmo arquivo [ci-cd.yml](.github/workflows/ci-cd.yml) supracitado.


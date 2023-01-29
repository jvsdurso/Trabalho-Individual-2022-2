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
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


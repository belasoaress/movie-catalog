# 🎬 Movie Catalog

API para gerenciamento de catálogo de filmes desenvolvida com FastAPI, utilizando PostgreSQL como banco de dados e Docker para conteinerização da aplicação.


## Pré-requisitos

Antes de executar o projeto, é necessário possuir:

* Docker Desktop
* Git

---

## Executando com Docker Compose

Para construir e iniciar todos os serviços:

```bash
docker compose up -d --build
```

Para verificar os containers em execução:

```bash
docker ps
```

---

## Parando a Aplicação

Parar os containers:

```bash
docker compose stop
```

Remover os containers:

```bash
docker compose down
```

---

## Serviços Disponíveis

### API

```text
http://localhost:8000
```

### Documentação Swagger gerada automaticamente

```text
http://localhost:8000/docs
```

### PgAdmin

```text
http://localhost:5050
```

---

## GitHub Actions

O projeto utiliza GitHub Actions para automação do processo de build e publicação da imagem Docker.

Sempre que houver um novo commit na branch principal (`main`), uma nova imagem Docker é construída e publicada automaticamente no GitHub Container Registry (GHCR).

---


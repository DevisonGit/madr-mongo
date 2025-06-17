# 📚 MADR – Meu Acervo Digital de Romances

Neste projeto vamos construir uma API que segue os mesmos moldes da que desenvolvemos durante o curso, porém, com outra proposta. Iremos fazer uma versão simplificada de um acervo digital de livros. Chamaremos de **MADR** (lê-se "Mader"), uma sigla para **"Meu Acervo Digital de Romances"**.

---

## 🧾 Descrição

A proposta do MADR é permitir o cadastro, listagem, atualização e remoção de livros em um acervo digital. A aplicação é baseada em uma API REST desenvolvida com **FastAPI** e utiliza **MongoDB** como banco de dados.

---

## 🚀 Funcionalidades

- 📚 Cadastrar novos livros
- 🔍 Buscar livros por título, autor ou gênero
- ✏️ Atualizar informações de livros
- 🗑️ Remover livros do acervo
- 🌐 API RESTful com documentação automática via Swagger

---

## ⚙️ Tecnologias utilizadas

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Pydantic](https://docs.pydantic.dev/) para validação de dados
- [Uvicorn](https://www.uvicorn.org/) como servidor ASGI
- [Docker](https://www.docker.com/)

---

## 📦 Requisitos

- Python 3.10+
- Poetry (ou pip)
- MongoDB
- Docker

---

## 🛠️ Instalação

```bash 
  # Clone o repositório
git clone https://github.com/DevisonGit/madr.git
cd madr

# Instale as dependências com Poetry
poetry install

# Ativar o ambiente 
eval $(poetry env activate)
```

## ▶️ Como usar
```bash
  # Iniciar a aplicação
task run
```
Acesse a documentação interativa da API em:  
📄 http://localhost:8000/docs

## 🧪 Executar os testes
```bash
  # Executar os testes
task test
```
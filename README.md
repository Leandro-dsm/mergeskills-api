# MergeSkills API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Docker](https://img.shields.io/badge/Docker-24.0-blue.svg)
![Swagger](https://img.shields.io/badge/Swagger-3.0-green.svg)

**API RESTful para plataforma de aprendizado de habilidades de desenvolvimento web**

[Documentação](#-documentação) • [Instalação](#-instalação) • [Endpoints](#-endpoints) • [Docker](#-docker)

</div>

---

## Sobre o Projeto

O **MergeSkills API** é uma API RESTful desenvolvida para gerenciar uma plataforma de aprendizado de habilidades de desenvolvimento web. O sistema permite gerenciar cursos, aulas, perguntas e o progresso dos usuários, fornecendo uma base sólida para aplicações de e-learning.

### Principais Funcionalidades

- ✅ **Gerenciamento de Cursos** - CRUD completo de cursos
- ✅ **Estrutura de Aulas** - Organização hierárquica de conteúdo
- ✅ **Sistema de Perguntas** - Banco de questões com múltipla escolha
- ✅ **Progresso do Usuário** - Acompanhamento de aprendizado
- ✅ **Documentação Automática** - Swagger/OpenAPI integrado
- ✅ **Containerização** - Ambiente isolado com Docker
- ✅ **Validação de Dados** - Schemas com Pydantic

---

## Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Descrição |
|-----------|--------|-------------|
| **Python** | 3.11 | Linguagem principal |
| **Flask** | 2.3.3 | Framework web |
| **SQLAlchemy** | 3.1.1 | ORM para banco de dados |
| **PostgreSQL** | 15 | Banco de dados relacional |
| **Pydantic** | 2.5.0 | Validação de dados |

### Ferramentas
| Tecnologia | Versão | Descrição |
|-----------|--------|-------------|
| **Docker** | 24.0+ | Containerização |
| **Flasgger** | 0.9.7.1 | Documentação Swagger |
| **python-dotenv** | 1.0.0 | Gerenciamento de variáveis |
| **psycopg2** | 2.9.9 | Driver PostgreSQL |

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.11** ou superior
- **PostgreSQL 15** (ou Docker)
- **Docker** e **Docker Compose** (opcional, mas recomendado)
- **Git** (para clonar o repositório)

---

## Instalação

### Opção 1: Com Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/Leandro-dsm/mergeskills-api.git
cd mergeskills-api

# Inicie os containers
docker-compose up --build

# Em outro terminal, popule o banco de dados
docker-compose exec web python seed.py

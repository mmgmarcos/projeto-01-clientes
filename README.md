# 📊 Pipeline de Dados de Clientes

Pipeline de dados desenvolvido em **Python** para demonstrar conceitos fundamentais de Engenharia de Dados, incluindo ingestão, validação, tratamento, qualidade de dados e persistência em PostgreSQL.

O projeto faz parte do **HomeLab Data & AI**, laboratório pessoal utilizado para estudos e desenvolvimento prático em Engenharia de Dados e Inteligência Artificial.

## 🎯 Objetivo

Construir um pipeline capaz de:

* Ler dados de clientes a partir de arquivo CSV;
* Validar a qualidade dos dados;
* Separar registros válidos e inválidos;
* Armazenar registros inválidos em uma área de quarentena;
* Carregar dados válidos no PostgreSQL;
* Realizar carga incremental utilizando **UPSERT**;
* Atualizar registros existentes sem duplicação;
* Manter credenciais do banco fora do código-fonte.

## 🏗️ Arquitetura

```text
                 clientes.csv
                      │
                      ▼
                Python / Pandas
                      │
                      ▼
                   Validação
                      │
              ┌───────┴───────┐
              │               │
              ▼               ▼
        Dados válidos    Dados inválidos
              │               │
              ▼               ▼
         PostgreSQL      Quarentena CSV
              │
              ▼
        Carga incremental
             UPSERT
```

## 🔄 Fluxo de processamento

### 1. Ingestão

Os dados são carregados a partir de:

```text
data/clientes.csv
```

utilizando Pandas.

### 2. Validação

O pipeline aplica regras de qualidade aos dados.

Para o campo `idade`, são considerados válidos valores entre **18 e 100 anos**.

Registros que não atendem à regra são classificados como inválidos.

### 3. Quarentena

Os registros inválidos são separados e armazenados em:

```text
data/clientes_quarentena.csv
```

Dessa forma, dados inconsistentes não são carregados na base principal.

### 4. Persistência

Os registros válidos são carregados no **PostgreSQL**.

### 5. Carga incremental

O pipeline utiliza **UPSERT** para tratar registros existentes.

```sql
ON CONFLICT (id_cliente)
DO UPDATE SET
    nome = EXCLUDED.nome,
    estado = EXCLUDED.estado,
    idade = EXCLUDED.idade
```

Quando o `id_cliente` não existe, o registro é inserido.

Quando o `id_cliente` já existe, seus dados são atualizados.

## 🧪 Exemplo de validação

Durante os testes, registros com idades fora do intervalo definido foram identificados e direcionados para a quarentena.

Exemplo:

```text
4, Ana Souza, SP, 150
5, Pedro Lima, PR, 17
9, Lucas Martins, MG, 200
```

Esses registros não são carregados na tabela principal.

## 🛠️ Tecnologias utilizadas

* Python
* Pandas
* SQL
* PostgreSQL
* SQLAlchemy
* python-dotenv
* Git

## 📂 Estrutura do projeto

```text
projeto-01-clientes/
│
├── data/
│   ├── clientes.csv
│   └── clientes_quarentena.csv
│
├── src/
│   ├── database.py
│   └── pipeline.py
│
├── .gitignore
├── .env
└── README.md
```

> O arquivo `.env` contém as configurações de acesso ao banco de dados e não é versionado no Git.

## 🔐 Configuração

As credenciais do PostgreSQL são armazenadas por meio de variáveis de ambiente:

```text
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```

O arquivo `.env` deve permanecer fora do controle de versão.

## ▶️ Execução

Com o ambiente virtual ativado e as dependências instaladas:

```bash
python src/pipeline.py
```

O pipeline:

1. Lê o arquivo CSV;
2. Valida os registros;
3. Gera o arquivo de quarentena;
4. Carrega os registros válidos no PostgreSQL;
5. Executa a carga incremental utilizando UPSERT;
6. Exibe os resultados no terminal.

## 📈 Status do projeto

### ✅ Implementado

* Leitura de CSV
* Validação de dados
* Separação de registros inválidos
* Quarentena
* Conexão com PostgreSQL
* Persistência dos dados
* Carga incremental
* UPSERT
* Proteção de credenciais com `.env`
* Versionamento com Git

### 🔄 Próximas evoluções

* Tratamento estruturado de exceções
* Logging
* Testes automatizados
* Validação de schema
* Melhorias de configuração
* Monitoramento
* Integração com APIs
* Orquestração do pipeline

## 📚 Conceitos de Engenharia de Dados

Este projeto demonstra, em escala educacional e de portfólio:

* Data Ingestion
* Data Validation
* Data Quality
* Data Transformation
* Data Quarantine
* Database Loading
* Incremental Loading
* UPSERT
* ETL
* Python para Engenharia de Dados
* PostgreSQL
* Versionamento com Git

## 🎓 Contexto

Projeto desenvolvido como parte da formação prática em **Engenharia de Dados**, utilizando o HomeLab Data & AI como ambiente de experimentação.

**Autor:** Marcos Moraes Garcia

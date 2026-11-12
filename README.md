# Python Data Persistence

Data persistence in Python: from a local SQLite database with `sqlite3` to a CRUD REST API with FastAPI and PostgreSQL.

This repository follows my learning path through data persistence in Python. Each stage lives in its own folder and builds on the previous one.

## Stages

| Stage | Folder | Status |
|---|---|---|
| SQLite with `sqlite3` | `sqlite/` | ✅ Done |
| REST API with FastAPI + PostgreSQL | `fastapi-postgres/` | 🚧 In progress |

---

## Stage 1 – SQLite

A small student enrollment system that talks to a SQLite database using only Python's standard library.

### Data model

```
estudantes                 matriculas
──────────                 ──────────
id (PK)      ◄──────────── estudante_id (FK)
nome                       id (PK)
idade                      nome_disciplina
```

Each enrollment (`matriculas`) belongs to one student (`estudantes`) through a foreign key.

### Features

| Function | Description |
|---|---|
| `conectar()` | Opens a connection to `escola.db` (creates the file if it does not exist) |
| `criar_tabela_estudantes()` | Creates the `estudantes` table |
| `criar_tabela_matriculas()` | Creates the `matriculas` table with a foreign key to `estudantes` |
| `criar_estudante(nome, idade)` | Inserts a student |
| `criar_matricula(estudante_id, nome_disciplina)` | Enrolls a student in a subject |
| `listar_estudantes()` | Lists all students |
| `listar_matriculas()` | Lists enrollments with the student's name, using a `JOIN` |

### Concepts practiced

- Connections, cursors, `execute`, `commit` and `close`
- `CREATE TABLE`, `INSERT`, `SELECT` and `JOIN`
- Primary and foreign keys
- Parameterized queries (`?` placeholders) to prevent SQL injection
- Separating the data layer (`db.py`) from the entry point (`main.py`)

### How to run

No external dependencies are needed: `sqlite3` ships with Python.

```bash
cd sqlite
python main.py
```

`main.py` creates the tables, inserts sample data and prints the results. The database file (`escola.db`) is generated automatically and is not versioned.

> Running `main.py` more than once inserts the sample data again, creating duplicate rows.

---

## Stage 2 – FastAPI + PostgreSQL

Coming next: a REST API for the same domain, using:

- **FastAPI** for the routes
- **SQLAlchemy** as the ORM
- **PostgreSQL** as the database, via **psycopg2**
- **Pydantic** for request and response validation
- **python-dotenv** to keep credentials out of the code

## Setup

```bash
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)
# source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
```

Database credentials for Stage 2 are read from a `.env` file, which is not versioned. See `.env.example` for the expected variables.

## Project structure

```
.
├── sqlite/
│   ├── db.py          # database functions
│   └── main.py        # demo entry point
├── fastapi-postgres/  # stage 2
├── requirements.txt
├── .env.example
└── .gitignore
```

# Python Data Persistence

Data persistence in Python: from a local SQLite database with `sqlite3` to a CRUD REST API with FastAPI and PostgreSQL.

This repository follows my learning path through data persistence in Python. Each stage lives in its own folder and builds on the previous one.

## Stages

| Stage | Folder | Status |
|---|---|---|
| SQLite with `sqlite3` | `sqlite/` | ✅ Done |
| REST API with FastAPI + PostgreSQL | `fastapi-postgres/` | ✅ Running |

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

The same student enrollment domain, now exposed as a REST API and persisted in PostgreSQL.

### Stack

- **FastAPI** – routes and automatic API docs
- **Uvicorn** – ASGI server
- **SQLAlchemy** – ORM: Python classes are mapped to database tables
- **PostgreSQL** – database, accessed through the **psycopg** driver
- **Pydantic** – request and response validation
- **python-dotenv** – loads credentials from a `.env` file, keeping them out of the code

### Project files

| File | Responsibility |
|---|---|
| `database.py` | Engine, session factory and declarative `Base` |
| `models.py` | SQLAlchemy models: how data is stored (tables) |
| `schemas.py` | Pydantic schemas: what goes in and out of the API (JSON) |
| `main.py` | FastAPI app, database session dependency and routes |

### Endpoints

| Method | Route | Description |
|---|---|---|
| `POST` | `/students` | Create a student |
| `GET` | `/students` | List students |
| `GET` | `/students/{id}` | Get a student by id |
| `PUT` | `/students/{id}` | Update a student |
| `DELETE` | `/students/{id}` | Delete a student and their enrollments |
| `POST` | `/enrollments` | Enroll a student in a course |
| `GET` | `/enrollments` | List enrollments |
| `GET` | `/enrollments/{id}` | Get an enrollment by id |
| `PUT` | `/enrollments/{id}` | Update an enrollment |
| `DELETE` | `/enrollments/{id}` | Delete an enrollment |

### How to run

**1. Install PostgreSQL** and create the database:

```sql
CREATE DATABASE escola;
```

**2. Configure the credentials.** Copy `.env.example` to `.env` and fill in your own PostgreSQL user and password:

```
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/escola
```

**3. Install the dependencies and start the server** (from the `fastapi-postgres/` folder, with the virtual environment active):

```bash
pip install -r ../requirements.txt
uvicorn main:app --reload
```

The tables are created automatically on startup.

**4. Open the interactive docs** at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to try every endpoint from the browser.

## Setup

```bash
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)
# source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
```

The `.env` file holds real credentials and is never versioned. See `.env.example` for the expected variables.

## Project structure

```
.
├── sqlite/
│   ├── db.py          # database functions
│   └── main.py        # demo entry point
├── fastapi-postgres/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

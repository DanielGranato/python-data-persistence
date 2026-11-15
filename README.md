# Python Data Persistence

Data persistence in Python: from a local SQLite database with `sqlite3` to a CRUD REST API with FastAPI and PostgreSQL, and on to modeling relationships between tables.

This repository follows my learning path through data persistence in Python. Each stage lives in its own folder and builds on the previous one.

## Stages

| Stage | Folder | Status |
|---|---|---|
| SQLite with `sqlite3` | `sqlite/` | ✅ Done |
| REST API with FastAPI + PostgreSQL | `fastapi-postgres/` | ✅ Done |
| Data modeling: one-to-one relationship | `fastapi-modeling/` | ✅ Done |

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

---

## Stage 3 – Data modeling

The same FastAPI + SQLAlchemy stack, now focused on **modeling relationships between tables**. This stage models a one-to-one relationship: each student has exactly one profile.

### Data model

```
students                   profiles
────────                   ────────
id (PK)      ◄──────────── student_id (FK, unique)
name                       id (PK)
email (unique)             age
                           address
```

- `student_id` in `profiles` is a foreign key marked `unique=True`, which is what enforces **one** profile per student at the database level.
- On the SQLAlchemy side, `relationship(..., uselist=False)` makes `student.profile` a single object instead of a list, and `back_populates` links both directions (`student.profile` and `profile.student`).
- `cascade="all, delete-orphan"` removes the profile when its student is deleted.

### Nested creation

The profile is created together with the student, in a single request. The client does not send a `student_id`, since the student has no id yet: `ProfileCreate` has no such field, and SQLAlchemy fills it in when the student is inserted.

```json
{
  "name": "Ana",
  "email": "ana@email.com",
  "profile": { "age": 20, "address": "Rua A, 10" }
}
```

The response returns the student with the profile nested inside it. Read routes use `joinedload` to fetch student and profile in a single query.

### Endpoints

| Method | Route | Description |
|---|---|---|
| `POST` | `/students` | Create a student together with their profile |
| `GET` | `/students` | List students with their profiles |
| `GET` | `/students/{id}` | Get a student with their profile |
| `PUT` | `/students/{id}` | Update a student and their profile |
| `DELETE` | `/students/{id}` | Delete a student and their profile |

Creating or updating a student with an email that is already registered returns `400`.

### Concepts practiced

- One-to-one relationships with `ForeignKey(unique=True)` and `relationship(uselist=False)`
- Bidirectional relationships with `back_populates`
- Cascade deletes with `delete-orphan`
- Nested Pydantic schemas for request and response bodies
- Eager loading with `joinedload`

### How to run

Create a database (for example `db_escola`), copy `fastapi-modeling/.env.example` to `fastapi-modeling/.env`, fill in the credentials, and start the server from that folder:

```bash
cd fastapi-modeling
uvicorn main:app --reload
```

The tables are created automatically on startup. Docs are available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Setup

```bash
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)
# source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
```

Each FastAPI stage has its own `.env`, which holds real credentials and is never versioned. See the `.env.example` next to it for the expected variables.

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
│   ├── main.py
│   └── .env.example
├── fastapi-modeling/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── main.py
│   └── .env.example
├── requirements.txt
└── .gitignore
```

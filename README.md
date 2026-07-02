# Document Grant Service

A REST API built with **FastAPI**, **SQLAlchemy 2.0 (Async)**, and **PostgreSQL** for managing document access grants.

Users can share documents with other users while assigning permissions (`VIEW`, `EDIT`, `ADMIN`) and expiration times. The service supports creating, listing, retrieving, revoking, and checking the status of grants.

---

## Tech Stack

* Python 3.11+
* FastAPI
* SQLAlchemy 2.0 (Async)
* asyncpg
* PostgreSQL
* Alembic
* Pydantic v2
* pytest
* pytest-asyncio
* Docker Compose

---

## Features

* Create document access grants
* List grants
* Retrieve a single grant
* Revoke grants
* Check grant status
* Async PostgreSQL support
* Alembic migrations
* Seed initial data
* Unit and Integration Tests

---

## Business Rules

* Expiration must be at least **1 minute** in the future.
* Only one **active** grant is allowed per **document + grantee**.
* Only the **creator** can revoke a grant.
* Revoked or expired grants cannot be revoked again.
* Revoked and expired grants remain stored permanently.

---

## Project Structure

```text
app/
│
├── api/
├── core/
├── crud/
├── db/
├── models/
├── schemas/
├── services/
├── main.py
│
alembic/
│
tests/
│
docker-compose.yml
requirements.txt
README.md
```

---

## API Endpoints

| Method | Endpoint                   | Description        |
| ------ | -------------------------- | ------------------ |
| POST   | `/grants`                  | Create a grant     |
| GET    | `/grants`                  | List grants        |
| GET    | `/grants/{grant_id}`       | Retrieve a grant   |
| DELETE | `/grants/{grant_id}`       | Revoke a grant     |
| GET    | `/grants/{grant_id}/check` | Check grant status |

---

## Database Schema

Schema:

```text
grants_svc
```

Tables:

* users
* documents
* grants

---

## Seed Data

The project seeds deterministic UUIDs for:

### Users

| Name  |
| ----- |
| Alice |
| Bob   |
| Carol |

### Documents

| Name            |
| --------------- |
| Q1 Report       |
| Product Roadmap |
| Budget 2026     |

Run the seed script after applying migrations.

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd document-grant-service
```

---

### 2. Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/grants_db
```

---

## Database Migration

Run migrations:

```bash
alembic upgrade head
```

---

## Seed Database

```bash
python -m seed
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

## Running with Docker

Build and start containers:

```bash
docker compose up --build
```

Run in background:

```bash
docker compose up -d
```

Stop containers:

```bash
docker compose down
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Run unit tests:

```bash
pytest tests/unit
```

Run integration tests:

```bash
pytest tests/integration
```

---

## Validation Rules

* Expiration time must be greater than one minute from the current UTC time.
* Duplicate active grants are rejected.
* Only the grant creator can revoke a grant.
* Revoked grants cannot be revoked again.
* Expired grants are treated as inactive.

---

## Future Improvements

* JWT Authentication
* Role-Based Access Control (RBAC)
* Pagination & Filtering
* Audit Logs
* Rate Limiting
* Structured Logging
* CI/CD Pipeline
* OpenTelemetry Tracing

---

## Author

Developed as part of a backend engineering assessment using FastAPI, SQLAlchemy Async, and PostgreSQL.

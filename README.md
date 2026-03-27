# DRC Minerals Production API

A production-grade REST API for the Democratic Republic of Congo minerals production dataset. Built with FastAPI and PostgreSQL, it exposes 270 records spanning 25 mineral types across 18 provinces from 2010 to 2024.

---

## Tech Stack

- **FastAPI** — high-performance Python web framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM and database toolkit
- **Alembic** — versioned database migrations
- **Pydantic** — data validation and serialization
- **pytest** — automated test suite

---

## Project Structure

```
drc-minerals-api/
├── app/
│   ├── api/v1/endpoints/     # Route handlers
│   ├── core/                 # Config and settings
│   ├── db/                   # Database session and base
│   ├── models/               # SQLAlchemy table definitions
│   ├── schemas/              # Pydantic request/response models
│   └── services/             # Business logic and queries
├── alembic/                  # Database migrations
├── scripts/                  # Seed script
├── tests/                    # pytest suite
├── main.py                   # Application entry point
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 14+

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/drc-minerals-api.git
cd drc-minerals-api
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/drc_minerals
APP_ENV=development
DEBUG=true
```

### 5. Create the database

```bash
psql -U postgres -c "CREATE DATABASE drc_minerals;"
```

### 6. Run migrations

```bash
alembic upgrade head
```

### 7. Seed the database

```bash
python3 scripts/seed.py
```

### 8. Start the server

```bash
uvicorn main:app --reload
```

Visit **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check and project info |
| `GET` | `/health` | Server status |
| `GET` | `/api/v1/minerals/` | List all minerals with filters and pagination |
| `GET` | `/api/v1/minerals/summary` | Aggregate stats by category, region, and year |
| `GET` | `/api/v1/minerals/{record_id}` | Get a single mineral record |
| `POST` | `/api/v1/minerals/` | Create a new mineral record |
| `PATCH` | `/api/v1/minerals/{record_id}` | Partially update a record |
| `DELETE` | `/api/v1/minerals/{record_id}` | Soft delete a record |

---

## Filtering and Pagination

The `GET /api/v1/minerals/` endpoint supports the following query parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `region` | string | Filter by province (case-insensitive partial match) |
| `category` | string | Filter by mineral category |
| `year` | integer | Filter by year recorded |
| `mining_status` | string | Filter by `Active`, `Inactive`, or `Artisanal` |
| `is_verified` | boolean | Filter by verification status |
| `skip` | integer | Pagination offset (default: 0) |
| `limit` | integer | Page size (default: 100, max: 500) |

Example:

```
GET /api/v1/minerals/?region=Haut-Katanga&category=Base Metal&is_verified=true
```

---

## Running Tests

```bash
python3 -m pytest tests/ -v
```

All 13 tests run against an isolated SQLite database — your PostgreSQL data is never affected.

---

## Dataset
The dataset was created and curated by **Qetsia Nkulu** as part of this project. Some records reference data sourced 
from the [Enough Project](https://enoughproject.org), a non-profit organization focused on conflict minerals and human rights in Central Africa.

 **Note:** The email addresses and organization names appearing in the audit trail fields (`created_by`, `updated_by`) are fictitious and used for illustrative purposes only. The dataset was intentionally designed to simulate the structure, complexity, and data quality patterns found in real production cloud data systems — including soft deletes, confidence scoring, data quality flags, and multi-source audit trails.


The dataset covers mineral production records from the Democratic Republic of Congo:

- **270 records** across 25 unique minerals
- **18 provinces** including Haut-Katanga, Lualaba, and North Kivu
- **2010–2024** year range
- Fields include confidence scores, data quality flags, audit trails, and soft delete support
The dataset covers mineral production records from the Democratic Republic of Congo:

- **270 records** across 25 unique minerals
- **18 provinces** including Haut-Katanga, Lualaba, and North Kivu
- **2010–2024** year range
- Fields include confidence scores, data quality flags, audit trails, and soft delete support

---

## Production Patterns Used

- **Soft deletes** — records are never hard-deleted; `is_active` and `deleted_at` preserve history
- **Alembic migrations** — every schema change is versioned and reproducible
- **Service layer** — business logic is fully separated from HTTP route handlers
- **Pydantic validation** — all input is validated before touching the database
- **Dependency injection** — database sessions are managed automatically per request
- **Environment-based config** — no hardcoded credentials anywhere in the codebase
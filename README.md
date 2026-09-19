# 🚀 SkillSync Backend (Labour Market Intelligence Platform)

Welcome to the **SkillSync** backend service. This project is built with **FastAPI** (high-performance async Python web framework), **SQLAlchemy 2.0** (Object-Relational Mapping / ORM), **PostgreSQL with pgvector** (relational and vector similarity storage), and **Alembic** (database migration and schema revision management).

---

## 💡 Important Concept: SQLAlchemy vs Alembic

In Python database development:

* **SQLAlchemy** is the **ORM (Object-Relational Mapper)**. It translates Python classes (`User`, `Skill`, `JobPosting`, etc.) into SQL tables and queries.

* **Alembic** is the **Database Migration Tool**. It inspects your SQLAlchemy models, tracks schema changes over time, and generates/applies version-controlled SQL migration scripts.

---

## 📂 Project Architecture — Which Part Does What?

Here is an overview of the directory structure and the responsibility of each module:

```text

backend/

├── .env                        # Local environment variables (DB URLs, secrets, app config)

├── .env.example                # Example template for environment variables

├── requirements.txt            # Python dependencies with pinned versions

├── alembic.ini                 # Configuration file for Alembic CLI

├── docker-compose.yml          # Optional Docker setup for PostgreSQL 16 + pgvector

│

├── alembic/                    # Database Migrations directory

│   ├── env.py                  # Alembic runtime script: connects to DB & binds Base.metadata

│   ├── script.py.mako          # Template for generating new migration scripts

│   └── versions/               # Generated migration scripts (e.g., 2e21c54ad8a6_initial_schema.py)

│

└── app/                        # Application source code

    ├── __init__.py

    ├── main.py                 # FastAPI application entry point, middleware & route mounting

    │

    ├── core/                   # Global configuration & security

    │   ├── __init__.py

    │   └── config.py           # Pydantic BaseSettings loading from .env with type safety

    │

    ├── database/               # Database connectivity & session management

    │   ├── __init__.py

    │   ├── base.py             # DeclarativeBase class that all models inherit from

    │   └── session.py          # SQLAlchemy Engine, SessionLocal factory, and get_db dependency

    │

    ├── models/                 # SQLAlchemy ORM Database Models (Entities)

    │   ├── __init__.py         # Re-exports all models for easy imports and Alembic tracking

    │   └── domain.py           # Domain models: User, RefreshToken, Skill, JobPosting, District, etc.

    │

    ├── schemas/                # Pydantic Schemas (DTOs - Data Transfer Objects)

    │   ├── __init__.py

    │   └── health.py           # Request / response validation & serialization models

    │

    ├── api/                    # HTTP Controllers / Routes

    │   ├── __init__.py

    │   └── routes/             # Grouped API route handlers

    │       ├── __init__.py

    │       └── health.py       # System health check route (/api/v1/health)

    │

    └── services/               # Business Logic Layer (Clean Architecture)

        └── __init__.py         # Houses services that handle complex logic away from API routes

```

### Module Breakdown:

1. **`app/main.py`**: Boots the FastAPI application, sets up metadata (`title`, `version`), and includes API routers under the `/api/v1` prefix.

2. **`app/core/config.py`**: Central source of truth for configuration (`Settings` class). Reads `.env`, validates types, and normalizes database connection strings for the `psycopg` (v3) driver.

3. **`app/database/base.py`**: Defines `Base(DeclarativeBase)` which tracks all SQLAlchemy table schemas in `Base.metadata`.

4. **`app/database/session.py`**: Creates the database engine connection pool, configures `SessionLocal`, and provides the `get_db()` dependency generator for FastAPI endpoints.

5. **`app/models/domain.py`**: Complete domain model definition with primary keys, indexes, foreign keys, relationships, and vector embeddings (`pgvector`).

6. **`app/schemas/`**: Pydantic schemas that validate inputs and shape API JSON responses, keeping database representations separate from API contracts.

7. **`app/api/routes/`**: Handles incoming HTTP requests, validates them with schemas, invokes services/queries, and returns responses.

8. **`app/services/`**: Keeps controllers thin by implementing business logic, calculations, or external API calls here.

9. **`alembic/env.py`**: Connects Alembic to `Base.metadata` and the active database, enabling `autogenerate` to detect schema changes.

---

## 🛠️ Step-by-Step Setup & Running

### 1. Activate the Virtual Environment

From the `backend/` folder:

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

*(Or in Command Prompt: `.\.venv\Scripts\activate.bat`)*

### 2. Install Project Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` if not already done:

```powershell
cp .env.example .env
```

Ensure your `DATABASE_URL` matches your PostgreSQL credentials:
```env
DATABASE_URL=postgresql+psycopg://postgres:2040@localhost:5432/apollo-skillsync
```

*(Note: If using the provided `docker-compose.yml`, the default database URL is `postgresql+psycopg://postgres:postgres@localhost:5432/kaushallens`)*

### 4. Run Database Migrations

Apply the existing database schema migrations to create all tables:

```powershell
alembic upgrade head
```

To create a new migration after modifying any model in `app/models/`:

```powershell
alembic revision --autogenerate -m "describe_your_changes"
alembic upgrade head
```

### 5. Start the FastAPI Development Server

From inside the `backend/` directory:
```powershell
uvicorn app.main:app --reload
```

* **API Root**: [http://localhost:8000/](http://localhost:8000/)

* **Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

* **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

* **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔍 Key Issues Identified & Fixed

During review of the initial setup, several critical issues were identified and resolved:

1. **`pgvector` Not Found in IDE / Python**:

   * **Cause**: Dependencies were installed globally in your system Python rather than inside the project's local virtual environment (`backend/.venv`).

   * **Fix**: Installed all packages from `requirements.txt` into `backend/.venv` so VS Code and the project interpreter resolve `pgvector` and all libraries properly.

2. **Foreign Key Table Name Mismatch (`NoReferencedTableError`)**:

   * **Cause**: `District`, `Sector`, and `Company` had singular `__tablename__` (`"district"`, `"sector"`, `"company"`), while other models referenced plural foreign keys (`districts.id`, `sectors.id`, `companies.id`).

   * **Fix**: Standardized all table names to plural (`districts`, `sectors`, `companies`), which is standard convention and aligned all foreign key references.

3. **Database Driver Prefix (`psycopg` v3 vs `psycopg2`)**:

   * **Cause**: `requirements.txt` specifies `psycopg==3.3.5` (the new psycopg v3). By default, SQLAlchemy interprets `postgresql://` as requiring the older `psycopg2`.

   * **Fix**: Added automatic driver normalization in `app/core/config.py` and `alembic/env.py` (`postgresql+psycopg://`), avoiding `ModuleNotFoundError: No module named 'psycopg2'`.

4. **Broken Alembic Configuration (`SQLModel` & `app.database.models`)**:

   * **Cause**: `alembic/env.py` imported `from sqlmodel import SQLModel` and `from app.database import models`, neither of which existed.

   * **Fix**: Updated `env.py` to import `Base` from `app.database.base` and `import app.models`, binding `target_metadata = Base.metadata`.

5. **Pydantic Settings Tuple Bug**:

   * **Cause**: `APP_NAME: str = "SkillSync",` and `DEBUG: bool = False,` had trailing commas, turning them into Python tuples and crashing Pydantic validation.

   * **Fix**: Removed trailing commas and added sensible defaults for optional settings.

6. **Session Engine Call Bug**:

   * **Cause**: In `app/database/session.py`, `settings = get_settings` was missing parentheses `()`, assigning the function itself rather than calling it.

   * **Fix**: Changed to `settings = get_settings()`.

7. **Module Import Paths in `main.py`**:

   * **Cause**: `from api.routes.health import router` failed when running the application from the `backend/` directory.

   * **Fix**: Updated imports to full package paths: `from app.api.routes.health import router`.

---

## ✅ Current Backend Status

The backend has progressed beyond the initial foundation. The following functionality has been implemented and/or integrated:

1. Authentication & Authorization

Added user authentication flow with registration and login.

Added password hashing using Argon2.

Added JWT-based authentication and token handling.

Added support for the Government user/role required by the platform.

Added/used the User and RefreshToken models for authentication state.

Added authentication-related schemas and API routes.

2. Database & Infrastructure

PostgreSQL database is configured with SQLAlchemy.

Alembic migrations are configured and working.

Docker/PostgreSQL setup is included.

pgvector is configured for future semantic/vector search functionality.

The domain model currently contains 19 database tables.

Seed data was added/used for foundational entities such as sectors and districts.

3. District CRUD

District management has been implemented with API support for:

Creating districts

Reading/listing districts

Updating districts

Deleting districts

District seed data is also available for development/testing.

4. Company CRUD

Company management has been added with:

Company Pydantic schemas

Company API routes

Company CRUD operations

Sector relationship through sector_id

Important: Companies depend on the sectors table through a foreign key, so sectors must exist before creating companies.

5. Project Structure

The backend now follows a clearer separation between:

models/ — database entities

schemas/ — request/response validation

api/routes/ — HTTP endpoints

services/ — business logic

database/ — database connection/session management

core/ — configuration and security

alembic/ — database migrations

## 🚧 Remaining / Next Backend Work

The following areas are still planned/in progress:

1. Job Management

Implement Job CRUD.

Connect companies with job postings.

Connect districts/locations with job postings.

2. Skills & Job Intelligence

Job/skill extraction.

Skill normalization.

Skill-demand analysis.

Skill-gap calculation between users and jobs.

3. Training System

Training/course database.

Training matching based on user skill gaps.

Government training/camp data and matching.

4. User Profiles

Expand user profiles with career information, experience, current job, completed training, and relevant skills.

Connect profile information to skill-gap and training recommendations.

5. Location & Labour-Market Intelligence

Location-based company/job discovery.

District/company/job relationships.

Labour-market data processing for the platform's reports.

6. Government Dashboard

APIs required by the government dashboard.

Aggregated job, skill, company, training, and labour-market information.

7. Semantic Search / Embeddings

Generate embeddings for jobs and skills.

Use pgvector for semantic similarity and matching once the required job and skill data pipelines are implemented.

## 📌 Development Notes

Keep database schema changes version-controlled through Alembic.

New models should be imported through app.models so Alembic can detect them.

API request/response structures should be defined through Pydantic schemas.

Business logic should remain in the services layer where appropriate rather than being placed directly inside route handlers.

Never commit real .env secrets or database passwords to the repository.
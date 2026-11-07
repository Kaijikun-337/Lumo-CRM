# Lumo CRM

A production-ready, asynchronous multi-tenant CRM engine and lead ingestion platform built with **FastAPI**, **SQLAlchemy**, and **Pydantic**.

Lumo CRM features dynamic payload parsing, strict tenant isolation across all endpoints, background task queueing with full payload audit logging, and an embedded single-page dashboard.

---

## Key Features

* **Multi-Tenant Security & Scoping**: Every resource (`Project`, `Source`, `Lead`, `Task`, `Milestone`) is bound to an authenticated `User` tenant. Queries are scoped at the database level to prevent cross-tenant data access.
* **Polymorphic Ingestion Pipeline**: Strategy-pattern architecture (`ParserFactory`) that dynamically switches normalization parsers based on incoming `Source` definitions (supporting JSON webhooks and CSV batch payloads).
* **Asynchronous Queueing & Audit Trail**: Webhook ingestion calls persist raw payloads to `raw_ingestion_logs` with a status of `PENDING` before delegating normalization to FastAPI `BackgroundTasks`, delivering immediate `202 Accepted` HTTP responses.
* **JWT & OAuth2 Authentication**: Secure user registration and password hashing powered by `bcrypt` and signed JSON Web Tokens (`pyjwt`).
* **Clean Configuration Management**: Centralized settings powered by `pydantic-settings` reading from `.env` files.
* **Automated Integration Test Suite**: Complete integration test coverage (`pytest`) running against an isolated, in-memory SQLite database (`sqlite:///:memory:`).
* **Embedded SPA Dashboard**: Built-in Tailwind CSS & Vanilla JavaScript dashboard featuring live REST API binding alongside an offline demo sandbox mode.

---

## Tech Stack

| Component | Technology |
| --- | --- |
| **Framework** | Python 3.13+, FastAPI |
| **Database & ORM** | SQLite, SQLAlchemy 2.0 |
| **Authentication** | OAuth2 Password Bearer, PyJWT, Bcrypt |
| **Validation & Settings** | Pydantic v2, Pydantic-Settings |
| **Testing** | Pytest, HTTPX, Starlette TestClient |
| **Frontend** | HTML5, Tailwind CSS, Vanilla JavaScript |

---

## Project Structure

```text
Lumo-CRM/
├── app/
│   ├── main.py              # Application entrypoint & router registry
│   ├── config.py            # Environment configuration via pydantic-settings
│   ├── database.py          # SQLAlchemy engine & session factory
│   ├── models.py            # Database models & relationship schemas
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── security.py          # Bcrypt hashing & JWT token handling
│   ├── dependencies.py      # OAuth2 bearer & get_current_user injection
│   ├── parsers/             # Ingestion strategy factory & parsers
│   │   ├── base.py
│   │   ├── csv_parser.py
│   │   ├── json_parser.py
│   │   └── factory.py
│   ├── services/            # Background worker functions
│   │   └── ingestion.py
│   ├── routers/             # API endpoint routers
│   │   ├── auth.py
│   │   ├── projects.py
│   │   ├── sources.py
│   │   ├── leads.py
│   │   ├── tasks.py
│   │   ├── milestones.py
│   │   └── ingest.py
│   └── tests/               # Pytest suite & in-memory database fixtures
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_parser.py
│       └── test_tenancy.py
├── index.html               # Embedded SPA Frontend Dashboard
├── .env                     # Environment variables
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Dependency manifest
└── README.md

```

---

## Quick Start

### 1. Environment Setup

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/Kaijikun-337/Lumo-CRM.git
cd Lumo-CRM

# Create and activate virtual environment
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Linux/macOS:
source .venv/bin/activate

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

*(Or install manually: `pip install fastapi uvicorn sqlalchemy passlib bcrypt pyjwt python-multipart pydantic-settings pytest httpx`)*

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_super_secret_jwt_key_change_in_production
DATABASE_URL=sqlite:///crm.db
ACCESS_TOKEN_EXPIRE_MINUTES=1440

```

### 4. Run the API Server

Start the Uvicorn ASGI server:

```bash
uvicorn app.main:app --reload

```

* **Swagger UI Documentation**: `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`
* **ReDoc Documentation**: `[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)`

### 5. Access the Dashboard

Open `index.html` directly in your web browser, or serve it using any local HTTP server. The dashboard will automatically connect to `[http://127.0.0.1:8000/api/v1](http://127.0.0.1:8000/api/v1)` and fall back to demo mode if the server is offline.

---

## Running Automated Tests

Run the integration test suite against an isolated in-memory database:

```bash
python -m pytest -v

```

---

## API Reference Overview

| Router | Method | Endpoint | Description | Auth Required |
| --- | --- | --- | --- | --- |
| **Auth** | `POST` | `/api/v1/auth/register` | Register a new user | No |
| **Auth** | `POST` | `/api/v1/auth/login` | Authenticate & retrieve JWT bearer token | No |
| **Projects** | `POST` | `/api/v1/projects/` | Create a new project tenant | Yes |
| **Projects** | `GET` | `/api/v1/projects/` | List isolated projects owned by user | Yes |
| **Sources** | `POST` | `/api/v1/sources/` | Register an ingestion source (CSV / Webhook) | Yes |
| **Sources** | `GET` | `/api/v1/sources/` | List registered ingestion sources | Yes |
| **Ingestion** | `POST` | `/api/v1/ingest/{source_id}` | Asynchronous raw payload ingestion | No |
| **Ingestion** | `GET` | `/api/v1/ingest/logs` | Fetch raw ingestion audit logs | Yes |
| **Leads** | `GET` | `/api/v1/leads/` | Fetch normalized leads directory | Yes |
| **Tasks** | `POST` | `/api/v1/tasks/` | Create a task linked to a project/lead | Yes |
| **Milestones** | `POST` | `/api/v1/milestones/` | Create project milestone | Yes |

---
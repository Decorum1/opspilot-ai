# OpsPilot AI

OpsPilot AI is an intelligent operations and predictive maintenance platform designed to help organizations monitor equipment, manage maintenance workflows, identify operational risks, and eventually use machine learning and AI to support maintenance decisions.

The project is being developed as a production-oriented backend system, with capabilities being added incrementally as the architecture evolves.

## Current Status

**Phase 1: Backend Foundations**

The first phase establishes the core API and equipment management system.

### Current Features

- FastAPI REST API
- Equipment registration
- Retrieve all equipment
- Retrieve individual equipment by ID
- Update equipment records
- Delete equipment records
- Persistent SQLite database storage
- Equipment data validation with Pydantic
- Equipment status and criticality validation
- Unique equipment serial numbers
- HTTP 404 handling for missing equipment
- HTTP 409 handling for duplicate serial numbers
- Modular API routing using FastAPI `APIRouter`
- Interactive API documentation with Swagger UI

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn
- Git

## Current Architecture

```text
opspilot-ai/
├── routers/
│   └── equipment.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Responsibilities

`main.py` initializes the FastAPI application and registers application routers.

`routers/equipment.py` contains the HTTP endpoints for equipment management.

`schemas.py` defines request validation and equipment data structures.

`models.py` defines the SQLAlchemy database model.

`database.py` configures the database engine and database sessions.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/equipment` | Create equipment |
| GET | `/equipment` | Retrieve all equipment |
| GET | `/equipment/{equipment_id}` | Retrieve equipment by ID |
| PUT | `/equipment/{equipment_id}` | Update equipment |
| DELETE | `/equipment/{equipment_id}` | Delete equipment |

## Running the Project Locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the API

```bash
python -m uvicorn main:app --reload
```

### 5. Open the API documentation

Once the server is running, open `/docs` from the local server address displayed by Uvicorn to access Swagger UI.

## Development Roadmap

Future phases are planned to introduce:

- PostgreSQL and database migrations
- Maintenance records and work orders
- User authentication and role-based access control
- Equipment sensor data ingestion
- Predictive maintenance machine learning
- Equipment failure-risk prediction
- AI maintenance copilot
- Retrieval-Augmented Generation (RAG)
- AI tool calling and agentic workflows
- Automated testing
- Docker
- CI/CD
- Cloud deployment
- Logging and monitoring
- Caching and background processing
- Performance and reliability improvements

## Vision

The long-term goal of OpsPilot AI is to connect traditional maintenance management with predictive machine learning and AI-assisted decision support in one integrated operations platform.

The system will evolve from equipment management into a platform capable of analyzing operational data, predicting maintenance risks, retrieving technical knowledge, and assisting maintenance teams with informed actions.

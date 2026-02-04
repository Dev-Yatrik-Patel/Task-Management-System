# FastAPI Task Management System

## Overview
This project is a production-style backend API built using FastAPI for managing tasks with user authentication. It demonstrates clean architecture, proper separation of concerns, and real-world backend development practices including database migrations, JWT authentication, and dependency injection.

The system allows users to register, authenticate, and manage their personal tasks through a RESTful API.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| API Framework | FastAPI |
| Server | Uvicorn |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Authentication | JWT (JSON Web Tokens) |
| Database | PostgreSQL |
| Password Hashing | Bcrypt |

---

## Project Structure

```
app/
├── core/
│   ├── config.py           # Environment & settings
│   ├── database.py         # DB engine & session
│   ├── security.py         # Password hashing & JWT
│   └── responses.py        # Standardized API responses
├── models/
│   ├── user.py             # SQLAlchemy User model
│   └── task.py             # SQLAlchemy Task model
├── schemas/
│   ├── user.py             # Pydantic user schemas
│   └── task.py             # Pydantic task schemas
├── routers/
│   ├── auth.py             # Authentication APIs
│   ├── user.py             # User-related APIs
│   └── task.py             # Task-related APIs
├── services/
│   ├── user_service.py     # User business logic
│   └── task_service.py     # Task business logic
├── dependencies/
│   ├── db.py               # DB session dependency
│   └── auth.py             # Auth dependency
├── migrations/             # Alembic migrations
│   └── versions/
│       └── 5aeb8d46629c_create_user_and_tasks_tables.py
├── tests/                  # Test files
├── alembic.ini            # Alembic configuration
├── main.py                # Application entry point
└── requirements.txt       # Project dependencies
```

---

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- PostgreSQL (or SQLite for development)
- pip package manager

### Step 1: Clone and Navigate
```bash
cd task-management-system
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/taskdb
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Step 5: Run Database Migrations
```bash
# Apply all migrations to create database tables
alembic upgrade head
```

### Step 6: Start the Server
```bash
# Run the development server
uvicorn app.main:app --reload
```

The API will be available at:
- **Base URL**: http://localhost:8000
- **Interactive API docs (Swagger)**: http://localhost:8000/docs
---

## API Endpoints

### Authentication
- POST `/auth/register`
- POST `/auth/login`

### User
- GET `/users/me`

### Tasks (Authenticated)
- POST `/tasks`
- GET `/tasks`
- GET `/tasks/{task_id}`
- PUT `/tasks/{task_id}`
- DELETE `/tasks/{task_id}`

---

## Database & Migrations

- PostgreSQL is used as the primary database
- Alembic manages schema migrations
- All schema changes are performed via migration scripts
- Direct table editing is avoided

### Common Alembic Commands

```bash
alembic revision --autogenerate -m "message"
alembic upgrade head
alembic downgrade -1
````

---

## Async vs Sync Design

* All API routes are defined using `async def`
* SQLAlchemy ORM operations are synchronous
* This design keeps the system simple while still benefiting from FastAPI’s async capabilities.
---

## Environment Configuration

* Sensitive configuration values (database URL, secret key) are loaded from environment variables
* `.env` file is supported via `pydantic-settings`
* No credentials are hardcoded in source code

---

## Key Learnings

* Structuring FastAPI projects for scalability
* Clean separation of concerns (routers, services, dependencies)
* JWT-based authentication fundamentals
* Alembic migrations and schema versioning
* Safe API design using Pydantic response models
---

## Possible Enhancements

* Refresh tokens
* Rate limiting
* Role-based access control
* Automated tests
  
---
**Note**: This project is built as part of a FastAPI practical assignment to demonstrate backend development skills including authentication, database design, API development, and production-ready code practices.
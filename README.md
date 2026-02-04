# FastAPI Task Management System

## Overview
This project is a production-style backend API built using FastAPI.  
It implements a task management system with user authentication, task ownership, and database migrations.

The focus of this project is correctness, clean architecture, and real-world backend practices rather than feature overload.

---

## Tech Stack

- FastAPI (API framework)
- Uvicorn (ASGI server)
- SQLAlchemy 2.x (ORM)
- Alembic (Database migrations)
- PostgreSQL (Database)
- Pydantic v2 (Validation & serialization)
- JWT (Token-based authentication)

---

## Project Structure

```
app/
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
├── models/
│   ├── user.py
│   └── task.py
├── schemas/
│   ├── user.py
│   ├── task.py
│   └── common.py
├── routers/
│   ├── auth.py
│   ├── user.py
│   └── task.py
├── services/
│   ├── user_service.py
│   └── task_service.py
├── dependencies/
│   ├── db.py
│   └── auth.py
├── migrations/
├── tests/
└── main.py
````

---

## Authentication Flow

1. User registers using email and password
2. Password is hashed using bcrypt
3. User logs in using OAuth2-compatible form data
4. Server returns a JWT access token
5. Token is sent in `Authorization: Bearer <token>` header
6. Protected routes validate token and load the current user

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
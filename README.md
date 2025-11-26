# Insta-Backend

A scalable, high-performance backend service mimicking core Instagram functionality, built with **Clean Architecture** and **Domain-Driven Design (DDD)** principles.

## 🚀 Tech Stack

- **Language**: Python 3.14+
- **Framework**: FastAPI (Async)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (Async)
- **Migrations**: Alembic
- **Authentication**: JWT (Argon2 password hashing)
- **Package Manager**: uv (recommended) or pip

## 🛠️ Prerequisites

- **Python 3.14+**
- **Docker & Docker Compose**
- **uv** (optional but recommended for dependency management)

## ⚡️ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Jayzhong/insta-backend.git
cd insta-backend
```

### 2. Environment Configuration
Create a `.env` file in the root directory. You can copy the example:
```bash
cp .env.example .env
```
Ensure the `.env` values match your database configuration (defaults provided in `.env.example` work with the Docker setup).

### 3. Install Dependencies

Using **uv** (Recommended):
```bash
uv sync
```

Using **pip**:
```bash
pip install .
```

### 4. Start Infrastructure
Launch the PostgreSQL database container:
```bash
docker-compose up -d
```

### 5. Run Database Migrations
Initialize the database schema:
```bash
# If using uv
uv run alembic upgrade head

# If using pip/venv
source .venv/bin/activate
alembic upgrade head
```

### 6. Start the Server
```bash
# If using uv
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# If using pip/venv
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Running Tests
```bash
# Execute all integration tests
uv run pytest tests/integration/
```

## 📖 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🏗️ Architecture

This project strictly follows **Clean Architecture** to ensure decoupling and testability. The code is organized into four concentric layers:

1.  **Domain** (`src/domain`): Pure business logic and entities. No external dependencies.
2.  **Application** (`src/application`): Use cases orchestrating the domain logic.
3.  **Interfaces** (`src/interfaces`): Adapters for the outside world (API routers, etc.).
4.  **Infrastructure** (`src/infrastructure`): Concrete implementations (Database, File Storage, Auth providers).

Dependencies only point **inwards**.
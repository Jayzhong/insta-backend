# Project Context: Insta-Backend

## 1. Overview
This project is a scalable, high-performance backend service mimicking core Instagram functionality. It is built with strict adherence to **Clean Architecture** and **Domain-Driven Design (DDD)** principles.

**Primary Goal**: Decouple business logic from frameworks, databases, and external interfaces.

## 2. Technology Stack
- **Language**: Python 3.14+
- **Web Framework**: FastAPI (Async)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0+ (Async)
- **Authentication**: JWT (Argon2 hashing), HTTPBearer
- **Validation**: Pydantic V2
- **Dependency Injection**: FastAPI `Depends`
- **Migrations**: Alembic
- **Package Manager**: `uv` (preferred) or `pip`

## 3. Architecture & Directory Structure
The project follows a strict 4-layer "Onion" architecture. **The Dependency Rule is absolute**: Source code dependencies can only point **inwards**.

```text
src/
├── domain/                         # LAYER 1 (Inner): Pure Enterprise Logic
│   ├── user/entity.py              # Pure Python Dataclasses (No Pydantic/ORM)
│   └── ...
├── application/                    # LAYER 2: Application Logic / Use Cases
│   ├── user/use_cases.py           # Orchestration logic
│   ├── user/dto.py                 # Pure Python DTOs
│   └── ...
├── interfaces/                     # LAYER 3: Interface Adapters (Driving)
│   ├── api/                        # FastAPI Routers, Pydantic Schemas
│   └── ...
└── infrastructure/                 # LAYER 4 (Outer): Frameworks & Drivers (Driven)
    ├── persistence/                # SQLAlchemy Repositories, ORM Models
    ├── services/                   # Concrete implementations (Auth, Storage)
    └── ...
```

## 4. Unified Development Mandates (AI Rules)

**⚠️ CRITICAL: AI Agents must follow these rules to prevent regression and architectural drift.**

### Rule 1: Strict Layer Isolation & Explicit Data Mapping
*   **Domain Layer**: MUST NOT import `fastapi`, `sqlalchemy`, or `pydantic`. Use standard Python libraries only.
*   **Data Flow**: Data moving between layers must be explicitly mapped.
    *   **Interface $	o$ Application**: Map Pydantic Schemas $	o$ Pure Dataclasses (DTOs).
    *   **Infrastructure $	o$ Domain**: Map ORM Models $	o$ Domain Entities.
*   **Prohibited**: Passing Pydantic models into Use Cases. Passing ORM models out of Repositories.

### Rule 2: The "Vertical Integration" Test Requirement
*   **Mandate**: Every new feature (Use Case) MUST include a corresponding **Integration Test**.
*   **Scope**: The test must verify the full request lifecycle: API Request $	o$ Database Persistence $	o$ API Response.
*   **Goal**: Catch "glue" bugs (e.g., missing commits, dependency injection errors) that unit tests miss.

### Rule 3: Explicit Persistence & Transaction Boundaries
*   **Mandate**: Database changes are not saved automatically.
*   **Implementation**: Explicitly call `await session.commit()` (or use a Unit of Work context manager) at the end of a state-changing operation.
*   **Constraint**: Never assume `session.flush()` is sufficient for persistence.

### Rule 4: Fail-Fast Configuration
*   **Mandate**: Application configuration (Env Vars) must be validated at startup using strongly-typed settings (e.g., `pydantic-settings`).
*   **Behavior**: The application must **crash immediately** with a descriptive error if critical config is missing, rather than failing vaguely at runtime.

### Rule 5: Robust Input Handling (Interface Layer)
*   **Mandate**: The API layer (Interface) is the first line of defense. It must handle client-side quirks before data reaches the Application layer.
*   **Specific Case**: Handle empty strings `""` sent by clients for optional fields (like avatars). Sanitize these to `None` in the Router/Dependency layer.

### Rule 6: Standardized Error Translation
*   **Domain Layer**: Raise pure Python custom exceptions (e.g., `UserNotFound`).
*   **Interface Layer**: Register global **Exception Handlers** in `main.py` to map Domain Exceptions to specific HTTP Status Codes (e.g., `UserNotFound` $	o$ 404).
*   **Constraint**: Do not return `HTTPException` directly from the Application/Domain layers.

## 5. Naming Conventions
| Concept | Style | Example | Location |
| :--- | :--- | :--- | :--- |
| **Domain Entity** | PascalCase | `User` | `src/domain/user/entity.py` |
| **DB Model** | `Model` suffix | `UserModel` | `src/infra/persistence/orm/user.py` |
| **Pydantic Schema** | `In`/`Out` suffix | `UserRegisterIn` | `src/interfaces/api/schemas/` |
| **Repository Impl** | `SQLAlchemy...` | `SQLAlchemyUserRepository`| `src/infra/persistence/repositories/` |

## 6. Operational Guide

### Running the Server
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations
```bash
uv run alembic upgrade head
```

## 7. Current Feature Status
- **Auth**: Registration (Argon2), Login (JWT), Profile Update.
- **UX Features**: Default Avatar Generation (`ui-avatars.com`), Explicit Avatar Deletion.
- **Infra**: PostgreSQL, Async SQLAlchemy, Python-Dotenv.

```
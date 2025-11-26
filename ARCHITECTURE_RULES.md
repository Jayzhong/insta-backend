# ARCHITECTURE\_RULES.md

## 1\. Project Overview & Philosophy

The goal of this project is to implements a backend system similar to Instagram using **Python 3.14+**, **FastAPI**, and **SQLAlchemy 2.0 (Async)**.

The core architectural philosophy is **Domain-Driven Design (DDD)** combined with **Clean Architecture**. The primary goal is to decouple business logic from frameworks, databases, and external interfaces.

**⚠️ IMPORTANT FOR AI ASSISTANT:** You must strictly adhere to the **Dependency Rule**: Source code dependencies can only point **inwards**. Nothing in an inner circle can know anything at all about something in an outer circle.

## 2\. Technical Stack Constraints

* **Language:** Python 3.14+
* **Web Framework:** FastAPI (Async)
* **ORM:** SQLAlchemy 2.0+ (Use `AsyncSession`, `Mapped[]` syntax, declarative base)
* **Validation:** Pydantic V2 (Strict mode preferred)
* **Database:** PostgreSQL
* **Dependency Injection:** FastAPI `Depends` mechanism

## 3\. Directory Structure & Layer Responsibilities

The project root is `src/`. You must strictly follow this 4-layer structure.

```text
src/
├── domain/                         # LAYER 1 (Innermost): Enterprise Logic
│   ├── common/                     # Shared Value Objects, Base Entities
│   ├── user/                       # Aggregate: User
│   │   ├── entity.py               # Pure Python Data Classes
│   │   ├── exceptions.py           # Business Exceptions
│   │   └── values.py               # Value Objects (e.g., UserID, Email)
│   └── ...
│
├── application/                    # LAYER 2: Application Logic / Use Cases
│   ├── common/                     # Interfaces (UoW, common DTOs)
│   ├── user/
│   │   ├── dto.py                  # Data Transfer Objects (Pure Python dataclasses)
│   │   └── use_cases.py            # Application Services / Interactors
│   └── ...
│
├── interfaces/                     # LAYER 3: Interface Adapters
│   ├── api/                        # Driving Adapters (Web)
│   │   ├── v1/
│   │   │   ├── routers/            # FastAPI Routes
│   │   │   └── schemas/            # Pydantic Models (Request/Response)
│   │   └── dependencies.py         # DI wiring
│   └── repositories/               # Driven Adapters (Data Access)
│       ├── abstracts/              # Abstract Base Classes / Protocols
│       └── impl/                   # Concrete SQLAlchemy Implementations
│
└── infrastructure/                 # LAYER 4 (Outermost): Frameworks & Drivers
    ├── config/                     # Environment variables
    ├── database/
    │   ├── main.py                 # Engine & Session setup
    │   └── models/                 # SQLAlchemy ORM Models
    └── storage/                    # S3, Redis implementations
```

-----

## 4\. Strict Development Rules

### Rule \#1: The "No Frameworks in Domain" Rule

* **Domain Layer (`src/domain`)**: Must NOT import `fastapi`, `sqlalchemy`, or `pydantic`.
* It should contain only standard Python libraries.
* **Reason**: The core business logic must survive framework changes.

### Rule \#2: Entity vs. Model Separation

* **Entities (`domain`)**: Pure Python `dataclasses` defining business behavior and state.
* **Models (`infrastructure`)**: SQLAlchemy classes defining database tables.
* **The Mapping**: You must write explicit mapper methods in the **Repository Implementation** layer (`src/interfaces/repositories/impl`) to convert `Model -> Entity` (when reading) and `Entity -> Model` (when saving).
* **Forbidden**: Never pass an SQLAlchemy Model to the Use Case or API layer.

### Rule \#3: Pydantic Isolation

* **Pydantic Models (`BaseModel`)**: allowed **ONLY** in `src/interfaces/api/schemas`.
* **DTOs**: The Application layer (`src/application`) must use standard Python `@dataclass` for data transfer, not Pydantic models.
* **Reason**: Pydantic is an I/O validation tool, not a business modeling tool.

### Rule \#4: Dependency Injection

* All dependencies (Repositories, Services, Unit of Work) must be defined as abstracts (Protocols) in `src/interfaces/repositories/abstracts` or `src/application`.
* Implementations are injected at runtime using FastAPI's `Depends` in `src/interfaces/api/dependencies.py`.
* **Do not** instantiate concrete repositories directly inside Use Cases.

### Rule \#5: Asynchronous First

* All I/O bound operations (Database, API calls, File Ops) must be `async`.
* Use `await session.execute()` style for SQLAlchemy 2.0.

-----

## 5\. Naming Conventions & Code Style

To avoid confusion between layers, adhere to these naming suffixes:

| Concept | Suffix/Style | Example | Location |
| :--- | :--- | :--- | :--- |
| **Domain Entity** | No suffix / PascalCase | `User` | `src/domain/user/entity.py` |
| **DB Model** | `Model` suffix | `UserModel` | `src/infra/database/models/user.py` |
| **Pydantic Schema** | `Request`/`Response` | `CreateUserRequest` | `src/interfaces/api/schemas/` |
| **App DTO** | `DTO` suffix | `CreateUserInputDTO` | `src/application/user/dto.py` |
| **Repository Interface**| `Repository` | `UserRepository` | `src/interfaces/repos/abstracts/` |
| **Repository Impl** | `SQLAlchemy...` | `SQLAlchemyUserRepository`| `src/interfaces/repos/impl/` |

## 6\. Error Handling Strategy

1. **Domain Layer**: Raise pure Python custom exceptions (e.g., `UserNotFound`, `InsufficientFunds`).
2. **Application Layer**: Let exceptions bubble up or catch and re-raise as App-specific exceptions.
3. **Interface Layer (API)**: Use a global `exception_handler` in FastAPI main config to catch Domain Exceptions and translate them into HTTP 4xx/5xx responses. Do not return HTTP responses directly from Use Cases.

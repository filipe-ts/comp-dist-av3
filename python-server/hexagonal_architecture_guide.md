# Hexagonal Architecture Project Guide (Python + FastAPI + GraphQL + SOAP + Supabase)

This document explains the recommended **project structure**, the purpose of each folder, and provides **examples** of what should go inside each layer when implementing a Python API that supports **GraphQL** and **SOAP** using **Ports & Adapters (Hexagonal Architecture)**.

---

# 📁 Project Structure Overview

```
src/
  domain/
    entities/
    services/
    exceptions/
  application/
    ports/
    use_cases/
  adapters/
    db/
    graphql/
    soap/
    http/
  config/
  main.py
```

Each top-level folder has a very specific role.

---

# 🧱 1. `domain/` — **Pure Business Logic** (No Frameworks Allowed)
The **domain layer** contains the business rules, pure and independent of any technology.

## ✔ What goes here?
- **Entities** (business objects)
- **Value Objects**
- **Domain services** (rules not tied to persistence)
- **Custom domain exceptions**

## 📁 `domain/entities/`
Contains the core data structures.

**Example:** `user.py`
```python
from dataclasses import dataclass

t@dataclass
class User:
    id: int
    name: str
    email: str
```

## 📁 `domain/services/`
Business logic that does not belong to a single entity.

**Example:** `email_validator.py`
```python
def validate_email_format(email: str) -> bool:
    return "@" in email
```

## 📁 `domain/exceptions/`
Exceptions that represent domain errors.

**Example:**
```python
class UserNotFound(Exception):
    pass
```

---

# 🧩 2. `application/` — **Use Cases + Ports (interfaces)**
The **application layer** orchestrates business workflows.

It does **not** know anything about FastAPI, Supabase, SOAP, etc.

## ✔ What goes here?
- **Ports** (interfaces or abstract classes)
- **Use Cases** (application logic)

---

## 📁 `application/ports/`
These define **interfaces** that the adapters must implement.

**Example:** `user_repository.py`
```python
from abc import ABC, abstractmethod

class UserRepository(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    async def create(self, user_data: dict):
        pass
```

This port allows us to swap databases easily.

---

## 📁 `application/use_cases/`
Use cases orchestrate domain logic.

**Example:** `get_user.py`

```python
from python_server.application.ports import UserRepository
from python_server.domain.exceptions import UserNotFound


async def get_user(user_id: int, repo: UserRepository):
    user = await repo.get_by_id(user_id)
    if not user:
        raise UserNotFound()
    return user
```

The use case only depends on **ports**, not on actual database code.

---

# 🔌 3. `adapters/` — Implementations of Ports + APIs
This is where **framework-specific** details live.

## ✔ What goes here?
- Database repository implementation
- HTTP controllers (FastAPI)
- GraphQL schema and resolvers
- SOAP service

Adapters implement the **Ports** from the application layer.

---

# 📁 `adapters/db/`
Implements the `UserRepository` using Supabase/Postgres.

**Example:** `supabase_user_repository.py`

```python
from python_server.application.ports import UserRepository
from supabase import create_client


class SupabaseUserRepository(UserRepository):
    def __init__(self, client):
        self.client = client

    async def get_by_id(self, user_id: int):
        result = (
            self.client.table("users")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return result.data
```

---

# 📁 `adapters/graphql/`
Contains the **GraphQL schemas**, **types**, and **resolvers**.

**Example:** `schema.py`

```python
import strawberry
from python_server.application.use_cases import get_user


@strawberry.type
class UserType:
    id: int
    name: str
    email: str


@strawberry.type
class Query:
    async def user(self, id: int) -> UserType:
        repo = get_repo()  # Provided by DI
        return await get_user(id, repo)


schema = strawberry.Schema(query=Query)
```

---

# 📁 `adapters/soap/`
Contains SOAP service definitions using **Spyne**.

**Example:** `soap_user_service.py`
```python
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11

class UserService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def get_user(ctx, user_id):
        repo = get_repo()
        user = repo.get_by_id(user_id)
        return user["name"]
```

---

# 📁 `adapters/http/`
FastAPI routes and dependency injection.

**Example:** `http_app.py`

```python
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from python_server.adapters.graphql import schema
from starlette.middleware.wsgi import WSGIMiddleware
from python_server.adapters.soap import soap_application

app = FastAPI()

# Mount GraphQL
app.include_router(GraphQLRouter(schema), prefix="/graphql")

# Mount SOAP
app.mount("/soap", WSGIMiddleware(soap_application))
```

---

# 🔧 4. `config/`
Stores configuration and DI setup.

**Examples:**
- `settings.py`
- `database.py`
- `container.py` (for dependency injection)

Example `settings.py`:
```python
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
```

---

# 🚀 5. `main.py`
Application entrypoint.

**Example:**

```python
from python_server.adapters.http import app

# This file is used by uvicorn:
# uvicorn src.main:app --reload
```

---

# 🎯 Summary Table

| Layer | Purpose | Technologies Here |
|-------|----------|-------------------|
| **domain** | Business rules | Pure Python |
| **application** | Use cases + ports | Pure Python |
| **adapters** | Framework details | FastAPI, Spyne, Supabase, Strawberry |
| **config** | Settings, DI | Pydantic, env vars |
| **main.py** | Startup | Uvicorn |

---

# Want a starter template?
I can generate a **complete project scaffold** with folders and placeholder files for you. Just ask!


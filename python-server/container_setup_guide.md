# Dependency Injection Guide — `container.py`

This document explains **how to create and structure a `container.py` file** for your Hexagonal Architecture project using FastAPI, GraphQL (Strawberry), SOAP (Spyne), and Supabase.

The goal is to centralize:
- **Database connections**
- **Repository instantiation**
- **Dependency Injection**
- **App-wide singletons**

This keeps all adapters clean and aligned with Ports & Adapters architecture.

---

# 📁 Where the file lives

```
src/
  config/
    container.py
    settings.py
```

- `settings.py`: environment variables, URLs, keys
- `container.py`: creates objects and exposes helper functions like `get_repo()`

---

# 🎯 Purpose of `container.py`

`container.py` acts as a **simple DI (Dependency Injection) container**.
Its job is to:

- Create shared instances (e.g., Supabase client)
- Instantiate the concrete implementations of ports
- Expose functions for retrieving these instances
- Allow easy mocking during tests

---

# 🧱 Example: `settings.py`

```python
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
```

---

# 📦 Full Example of `container.py`

```python
from supabase import create_client
from adapters.db.supabase_user_repository import SupabaseUserRepository
from application.ports.user_repository import UserRepository
from config.settings import SUPABASE_URL, SUPABASE_KEY

# -----------------------------
# 1. Create external SDK clients
# -----------------------------

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# 2. Instantiate Adapters
# -----------------------------

# Repository implementing the UserRepository port
user_repository: UserRepository = SupabaseUserRepository(supabase_client)

# -----------------------------
# 3. Functions exposed to adapters and use cases
# -----------------------------

def get_user_repository() -> UserRepository:
    """
    Returns the instance of the user repository.
    Used by GraphQL resolvers, SOAP services, and HTTP routes.
    """
    return user_repository
```

---

# 🧠 How Other Layers Use This

## ✔ GraphQL Resolver

```python
from config.container import get_user_repository

@strawberry.type
class Query:
    async def user(self, id: int) -> UserType:
        repo = get_user_repository()
        return await get_user(id, repo)
```

---

## ✔ SOAP Service

```python
from config.container import get_user_repository

class UserService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def get_user(ctx, user_id):
        repo = get_user_repository()
        user = repo.get_by_id(user_id)
        return user["name"]
```

---

## ✔ REST Route (FastAPI)

```python
from fastapi import Depends
from config.container import get_user_repository

@app.get("/users/{user_id}")
async def get_user_route(user_id: int, repo = Depends(get_user_repository)):
    return await get_user(user_id, repo)
```

---

# 🔁 Why not instantiate inside each resolver?

Because that violates hexagonal architecture:

- Tight coupling with Supabase
- Hard to test
- Hard to swap DB implementation

`container.py` keeps everything clean and modular.

---

# 🧪 Testing Example

In tests, you can override the DI easily:

```python
from adapters.db.fake_user_repository import FakeUserRepository
import config.container as container

container.user_repository = FakeUserRepository()
```

Now **all** resolvers automatically use the fake repository — no code changes required.

---

# ✔ Summary

`container.py` should:

| Responsibility | Purpose |
|----------------|---------|
| Create external clients | Supabase, Redis, etc. |
| Instantiate repository adapters | `SupabaseUserRepository` |
| Expose DI functions | `get_user_repository()` |
| Allow testing overrides | swap in-memory repositories |

This file becomes the **central brain** for instantiating infrastructure dependencies.

---

If you want, I can also generate:
- A version using **Pydantic Settings**
- A more advanced container using **Dependency Injection frameworks** like `punq` or `wired`
- A starter file tree with all placeholder files


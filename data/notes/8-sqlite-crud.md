# FastAPI + SQLite CRUD Guide (Step‑by‑Step)

**Goal:** connect FastAPI to SQLite using SQLAlchemy (ORM), implement full CRUD for a `User` resource, and understand how it all fits together. This guide uses synchronous SQLAlchemy (simple and ideal for learning). Later you can move to async patterns.

---

## Prerequisites

- Python 3.10+ installed.
- Basic familiarity with Python and virtual environments.
- `pip` available.

---

## 1 — Project setup

```bash
# create project folder
mkdir fastapi-sqlite-crud
cd fastapi-sqlite-crud

# create virtualenv (optional but recommended)
python -m venv .venv
# activate: Windows: .venv\Scripts\activate ; mac/linux: source .venv/bin/activate

# install dependencies
pip install fastapi uvicorn sqlalchemy pydantic alembic python-multipart
# (optional for dev) pip install watchgod
```

**Why these packages?**
- `fastapi` : web framework
- `uvicorn` : ASGI server
- `sqlalchemy` : ORM and DB toolkit
- `pydantic` : FastAPI uses it for request/response validation
- `alembic` : DB migrations

---

## 2 — Folder layout (recommended)

```
fastapi-sqlite-crud/
├─ alembic/               # will be created by alembic init (migrations)
├─ app/
│  ├─ main.py
│  ├─ database.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ crud.py
│  └─ routers/
│     └─ users.py
└─ requirements.txt
```


---

## 3 — `database.py` — SQLAlchemy engine & session

Create `app/database.py`.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# connect_args required only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal class will be used to create DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

**Notes:**
- `check_same_thread=False` is required for SQLite when using in multiple threads (FastAPI's default workers).
- `SessionLocal()` will provide session objects.

---

## 4 — `models.py` — define the ORM model(s)

Create `app/models.py`.

```python
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
```

**Explanation:**
- `Base` is the declarative base; subclasses become tables.
- `index=True` speeds up lookups; `unique=True` enforces uniqueness.

---

## 5 — `schemas.py` — Pydantic models (validation)

Create `app/schemas.py`.

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
```

**Why `orm_mode = True`?**
This tells Pydantic to read data from ORM objects (SQLAlchemy models) directly.

---

## 6 — `crud.py` — DB access functions

Create `app/crud.py`. Split database logic from web layer for testability.

```python
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# Create
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(username=user.username, email=user.email, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read single
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

# Read by username
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

# Read many
def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

# Update
def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    # apply updates only for provided fields
    for field, value in user_in.__dict__.items():
        if value is not None:
            setattr(db_user, field, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete
def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
```

**Notes:**
- Always `commit()` after writes. `db.refresh()` loads generated fields (like `id`).
- Keep business logic out of your router.

---

## 7 — Dependency for DB sessions in FastAPI

Create a dependency in `app/database.py` or new `app/deps.py`. We'll add to `database.py` for simplicity.

```python
# add to app/database.py
from typing import Generator

# existing imports above

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Use `Depends(get_db)` in routes to get a DB session for the request.

---

## 8 — `routers/users.py` — API endpoints

Create `app/routers/users.py`.

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut, status_code=201)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # check duplicates
    if crud.get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    user = crud.create_user(db, user_in)
    return user

@router.get("/", response_model=List[schemas.UserOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=schemas.UserOut)
def patch_user(user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}
```

**Notes:**
- Use `response_model` for automatic response validation and docs.
- Use HTTP status codes and exceptions to communicate errors.

---

## 9 — `main.py` — wire up the app

Create `app/main.py`.

```python
from fastapi import FastAPI
from .database import engine, Base
from .routers import users

# create tables (for learning/demo). For production, use Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + SQLite CRUD Example")

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Hello — FastAPI + SQLite CRUD"}
```

**Important:**
`Base.metadata.create_all` will create tables automatically using your models. It’s fine for learning, but **use Alembic for real projects**.

---

## 10 — Run the app

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to see the interactive Swagger UI and test endpoints.

---

## 11 — Example requests (curl)

**Create user**
```bash
curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{"username":"alice","email":"alice@example.com","full_name":"Alice"}'
```

**Get users**
```bash
curl "http://127.0.0.1:8000/users/"
```

**Get single user**
```bash
curl "http://127.0.0.1:8000/users/1"
```

**Update user (partial)**
```bash
curl -X PATCH "http://127.0.0.1:8000/users/1" -H "Content-Type: application/json" -d '{"full_name":"Alice Smith"}'
```

**Delete user**
```bash
curl -X DELETE "http://127.0.0.1:8000/users/1"
```

---

## 12 — Alembic quickstart (migrations)

1. Initialize alembic:

```bash
alembic init alembic
```

2. Configure `alembic.ini`: set `sqlalchemy.url = sqlite:///./app.db` (or use env var pattern).

3. Edit `alembic/env.py` to import your `Base` and set target metadata. Replace or edit the section where `target_metadata` is defined:

```python
from app.database import Base
from app import models  # ensure models are imported so they are registered

target_metadata = Base.metadata
```

4. Create a revision from models:

```bash
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

**Tip:** When using packages, ensure `PYTHONPATH` allows alembic to import `app` (run from project root or set `env` accordingly).

---

## 13 — Testing & tips

- Use `TestClient` from `fastapi.testclient` to write tests for your endpoints.
- Keep CRUD functions small and test them directly (unit test) by creating a temporary SQLite DB (use `sqlite:///:memory:`) and a separate `SessionLocal`.

Example minimal test sketch:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    r = client.post('/users/', json={"username":"bob","email":"bob@example.com"})
    assert r.status_code == 201
    assert r.json()['username'] == 'bob'
```

---

## 14 — Common pitfalls & debugging

- **`sqlite3.OperationalError: unable to open database file`**: check path and permissions. Use absolute path if needed.
- **`IntegrityError` on unique constraint**: handle by checking duplicates or catching the exception.
- **Threading issues**: `check_same_thread=False` usually resolves common SQLite thread errors.
- **Migrations not detecting changes**: ensure models are imported in `env.py`.

---

## 15 — Next steps (authentication & beyond)

Once comfortable with the CRUD flow, add:
- Authentication (JWT with `python-jose`, `passlib` for password hashing).
- Authorization (roles, scopes).
- Asynchronous DB access (SQLAlchemy 1.4 async + `Databases` or `SQLModel`).
- Use `Alembic` migration scripts in CI.

---

## 16 — Quick reference: file summary

- `database.py` : engine, SessionLocal, Base, `get_db()` dependency
- `models.py` : SQLAlchemy ORM classes
- `schemas.py` : Pydantic models for request/response
- `crud.py` : functions to interact with DB (create, read, update, delete)
- `routers/users.py` : HTTP endpoints using `Depends(get_db)`
- `main.py` : app startup and router registration

---

If you want, I can:
- convert this document to a downloadable PDF,
- show you a ready-to-run GitHub-style project tree with all files filled,
- or extend it with JWT auth and password hashing next.

Happy coding — tell me which follow-up you'd like!


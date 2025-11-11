---

# 🧠 FastAPI Journey – Day 8–9: SQLAlchemy Setup & CRUD API

---

## 🎯 **Goal of These Days**

You’ll learn to:

* Connect FastAPI with a real database.
* Use **SQLAlchemy ORM** to model your data (like `User`).
* Use **Alembic** for database migrations.
* Build **complete CRUD APIs** for `/users`.

---

## 🧩 Why SQLAlchemy?

> **SQLAlchemy** = SQL + ORM + Power.

It is both:

1. **Core SQL toolkit** (low-level queries), and
2. **ORM (Object Relational Mapper)** — allows Python classes ↔ SQL tables mapping.

As an **AI Engineer**, you’ll use databases for:

* Storing users, API logs, model predictions, dataset metadata, etc.
* Managing experiments and results (think MLOps tools like MLflow).

---

## 🧱 Step 1: Install Required Packages

```bash
pip install sqlalchemy alembic psycopg2-binary
```

> Use `sqlite` for learning (lightweight, no setup).

---

## ⚙️ Step 2: Create Project Structure

```
fastapi_app/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
└── crud.py
```

---

## 🧩 Step 3: Configure Database Connection (`database.py`)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite URL (you can switch to PostgreSQL later)
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# Connect to database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()
```

### 💡 Explanation:

* `create_engine()` → connects SQLAlchemy to DB.
* `SessionLocal()` → handles transactions (open, commit, close).
* `Base` → parent for all your models.

---

## 🧍‍♂️ Step 4: Create User Model (`models.py`)

```python
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
```

### 🧠 ORM Concept:

Each `User` object maps to a **row in the `users` table.**
Each **attribute** → column in the table.

---

## 📦 Step 5: Create Schemas (Pydantic Models) (`schemas.py`)

These define **data validation** for API requests & responses.

```python
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
```

### 💡 Why `orm_mode = True`?

So FastAPI can convert SQLAlchemy models → JSON responses easily.

---

## 🧰 Step 6: CRUD Operations (`crud.py`)

```python
from sqlalchemy.orm import Session
from . import models, schemas

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
```

---

## 🚀 Step 7: Connect Everything in `main.py`

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users CRUD API")

# Dependency - creates & closes DB session automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}", response_model=schemas.UserResponse)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## ⚡ Step 8: Run the App

```bash
uvicorn fastapi_app.main:app --reload
```

✅ Open your browser → `http://127.0.0.1:8000/docs`

You can now:

* `POST /users` → Create a new user
* `GET /users` → List all users
* `GET /users/{id}` → Fetch by ID
* `DELETE /users/{id}` → Delete user

---

## 🧩 Step 9: Database Migrations with Alembic

### Why Alembic?

When your model changes (e.g., adding a new column), Alembic handles **DB schema versioning** safely — no manual edits.

### Setup Alembic

```bash
alembic init alembic
```

### Edit `alembic.ini`

Change:

```
sqlalchemy.url = sqlite:///./users.db
```

### Edit `alembic/env.py`

Add:

```python
from fastapi_app.database import Base
from fastapi_app.models import *
target_metadata = Base.metadata
```

### Run Migrations

```bash
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

---

## 🧠 Deep Insights (AI Engineer’s Perspective)

| Concept                  | Why It Matters in AI/ML Apps                                                      |
| ------------------------ | --------------------------------------------------------------------------------- |
| **SQLAlchemy ORM**       | Use it to store experiment results, hyperparameters, or fine-tuned model metrics. |
| **Alembic migrations**   | Track schema changes over ML lifecycle (new dataset columns, new metadata).       |
| **FastAPI CRUD**         | Easily build internal APIs for model management or dataset tracking dashboards.   |
| **Database abstraction** | Switch between SQLite (local), PostgreSQL (cloud), or MySQL seamlessly.           |

---

## 🧪 Practice Ideas

1. Add `update_user` route (PUT).
2. Add column `role: str` in `User` and apply Alembic migration.
3. Secure passwords using `bcrypt`.
4. Integrate with **JWT Auth** (Day 10 topic).
5. Replace SQLite with PostgreSQL (for production/AI pipelines).

---

## 🧾 Summary Cheat Sheet

| Step | File          | Purpose                             |
| ---- | ------------- | ----------------------------------- |
| 1️⃣  | `database.py` | DB connection & Base                |
| 2️⃣  | `models.py`   | ORM models                          |
| 3️⃣  | `schemas.py`  | Pydantic validation                 |
| 4️⃣  | `crud.py`     | Logic for Create/Read/Update/Delete |
| 5️⃣  | `main.py`     | API routes                          |
| 6️⃣  | Alembic       | Database migrations                 |

---



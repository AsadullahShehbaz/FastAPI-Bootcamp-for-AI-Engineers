Gotcha! Here’s a **step-by-step simple guide to adding password hashing for authentication** to your FastAPI app — designed like a student-friendly tutorial:

---

### Step 1: Add a `password` column to your User model

* You need to store a **hashed password**, not plaintext.
* So, add a `password` column in your `User` ORM model.

```python
from sqlalchemy import Column, String, Integer

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # <-- Add this line
```

---

### Step 2: Update your `UserCreate` Pydantic model to accept `password`

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  # <-- Add this line
```

---

### Step 3: Install and import **passlib** for hashing passwords

* Use `passlib`'s `bcrypt` hashing scheme (industry standard, secure)
* Install it in your terminal:

```bash
pip install passlib[bcrypt]
```

* Import the hashing utility in your code:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

---

### Step 4: Create helper functions to hash and verify passwords

```python
# Hash password before saving to DB
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify plain password against hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

---

### Step 5: Hash the password before creating a new user in `/create` endpoint

Update your user creation logic:

```python
@app.post("/create", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail='Email already exists')
    
    hashed_pwd = hash_password(user.password)  # Hash password here
    db_user = User(name=user.name, email=user.email, password=hashed_pwd)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

---

### Step 6: (Optional) Create a login endpoint to verify credentials

```python
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    return {"message": "Login successful!"}
```

---

### Recap in Student Style:

* **Add password column** in your DB model to store hashed passwords.
* **Accept password input** in your Pydantic model.
* **Use passlib’s bcrypt** to hash and verify passwords safely.
* **Hash password before saving** to DB.
* (Optional) Make a **login route** to check credentials.

---


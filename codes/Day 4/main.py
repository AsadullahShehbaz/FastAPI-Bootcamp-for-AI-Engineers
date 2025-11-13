from fastapi import FastAPI, Depends, HTTPException , Request 
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from database import engine, Base, get_db, Session
import models 
from models import User
from schemas import UserCreate, UserResponse, UserUpdate, LoginIn
from auth_hashing import get_password_hash, verify_password
from logging_config import logger 

# Define App 
app = FastAPI()

# Create orm model using declarative base & bind with engine 
models.Base.metadata.create_all(bind=engine)
logger.info("FastAPI app initialized and ORM tables created")

# Simple Root Endpoint
@app.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {"Message": "Welcome to Students Management System API", "Name": "Ayan Ahmed", "Goal": "AI Engineer"}

# Simple Health Endpoint
@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

# Read Users Endpoint 
@app.get('/read', response_model=list[UserResponse])
async def read_users(db: Session = Depends(get_db)):
    logger.info("Fetching all users from DB")
    users = db.query(User).all()
    logger.debug(f"Found {len(users)} users")
    return users

# Read User with ID Endpoint 
@app.get('/read/{user_id}')
async def read_user(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Fetching user with ID {user_id}, skip={skip}, limit={limit}")
    users = db.query(User).offset(skip).limit(limit).all()
    if not users:
        logger.warning(f"No users found for ID {user_id}")
    return users

# Create User Endpoint 
@app.post('/create', response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to create user with email: {user.email}")
    if db.query(User).filter(User.email == user.email).first():
        logger.warning(f"User creation failed: email {user.email} already registered")
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created successfully with ID {db_user.id}")
    return db_user

# Update User Endpoint 
@app.put('/update/{user_id}', response_model=UserResponse)
async def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating user ID {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"Update failed: User ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.name is not None:
        logger.debug(f"Updating name to: {user_in.name}")
        user.name = user_in.name
    if user_in.email is not None:
        exists = db.query(User).filter(User.email == user_in.email).first()
        if exists and exists.id != user_id:
            logger.warning(f"Update failed: Email {user_in.email} already registered to another user")
            raise HTTPException(status_code=400, detail="Email already registered")
        logger.debug(f"Updating email to: {user_in.email}")
        user.email = user_in.email
    db.commit()
    db.refresh(user)
    logger.info(f"User ID {user_id} updated successfully")
    return user

# Delete User Endpoint
@app.delete('/delete/{user_id}', response_model=UserResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting user ID {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"Delete failed: User ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    logger.info(f"User ID {user_id} deleted successfully")
    return user

# Login Endpoint
@app.post('/login')
async def login(data: LoginIn, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {data.email}")
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        logger.warning(f"Login failed for email: {data.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    logger.info(f"User ID {user.id} logged in successfully")
    return {
        "message": "✅ Login successful",
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
    }


# Custom Validation Error Handler 
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error for request : {request.url.path}, exception {exc}")
    return JSONResponse(
        status_code=422,
        content= {
            "error":"validation_error",
            "detail":exc.errors(),
            "body":exc.body,
        },
    )
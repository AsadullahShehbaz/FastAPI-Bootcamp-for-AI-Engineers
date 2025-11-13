from fastapi import FastAPI,Depends,HTTPException
from database import engine,Base,get_db,Session
import models 
from models import User , UserCreate , UserResponse , UserUpdate

# Define App 
app = FastAPI()

# Create orm model using declarative base & bind with engine 
models.Base.metadata.create_all(bind=engine)

# Simple Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI - v1 minimal"}

# Simple Heath Endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Read Users Endpoint 
@app.get('/read',response_model=list[UserResponse])
async def read_users(db : Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Read User with ID Endpoint 
@app.get('/read/{user_id}')
async def read_user(user_id : int ,skip : int = 0, limit : int = 10,db : Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()


# Create User Endpoint 
@app.post('/create',response_model=UserResponse,status_code=201)
async def create_user(user : UserCreate,db : Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        return HTTPException(status_code=400, detail="Email already registered")
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Update User Endpoint 
async def update_user(user_id : int , user_in : UserUpdate , db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.name is not None:
        user.name = user_in.name
    if user_in.email is not None:
        exists = db.query(User).filter(User.email == user_in.email).first()
        if exists and exists.id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = user_in.email
    db.commit()
    db.refresh(user)
    return user

# Delete User Endpoint
@app.delete('/delete/{user_id}')
async def delete_user(user_id : int ,response_model=UserResponse, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user
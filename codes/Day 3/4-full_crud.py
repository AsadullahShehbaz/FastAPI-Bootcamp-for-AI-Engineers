from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel,EmailStr
from typing import List,Optional

from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base , sessionmaker,Session

DB_URL = 'sqlite:///./students.db'

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,index=True,nullable=False)
Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
        name:str
        email:EmailStr

class UserResponse(BaseModel):
      id : int
      name : str
      email : EmailStr
      class Config:
            orm_mode = True

class UserUpdate(BaseModel):
      name : Optional[str] = None
      email : Optional[EmailStr] = None 

app = FastAPI()

def get_db():
      db = SessionLocal()
      try:
            yield db 
      finally:
            db.close()
@app.get('/')
def welcome():
      return {
            "Name":"Ayan Ahmed",
            "Level":"6"
      }


@app.post("/create",response_model=UserResponse)
def create_user(user:UserCreate,db:Session = Depends(get_db)):
      if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400,detail='Email already exists')
      db_user = User(name=user.name,email=user.email)
      db.add(db_user)
      db.commit()
      db.refresh(db_user)
      return db_user


@app.get("/read",response_model=List[UserResponse])
def read_user(skip:int = 0 , limit:int=5 , db:Session = Depends(get_db)):
      return db.query(User).offset(skip).limit(limit).all()

@app.get('/read/{user_id}',response_model=UserResponse)
def read_user(user_id:int,db:Session = Depends(get_db)):
      user = db.query(User).filter(User.id == user_id).first()
      if not user:
            raise HTTPException(status_code=404,detail='User not found')
      return user

@app.put("/update/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
      user = db.query(User).filter(User.id == user_id).first()
      if not user:
            raise HTTPException(status_code=404,detail='User not Found')
      if user_in.name is not None:
            user.name = user_in.name
      if user_in.email is not None:
            if db.query(User).filter(User.email == user_in.email).first():
                  raise HTTPException(status_code=404,detail='Email already in use')
            user.email = user_in.email
      db.commit()
      db.refresh(user)
      return user

@app.delete('/delete/{user_id}')
def delete_user(user_id : int , db:Session = Depends(get_db)):
      user = db.query(User).filter(User.id == user_id).first()
      if not user:
            raise HTTPException(status_code=404,detail='User not found')
      db.delete(user)
      db.commit()
      return user 
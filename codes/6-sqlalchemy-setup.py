from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel,EmailStr
from typing import List,Optional

from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base , sessionmaker,Session

DB_URL = 'sqlite:///./students.db'

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
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


from sqlalchemy import Column, Integer, String
from pydantic import BaseModel,EmailStr
from typing import Optional
from database import Base

# Create ORM Model for DB 
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

# Create Pydantic Model for User Creation Endpoint 
class UserCreate(BaseModel):
    name:str
    email : EmailStr 

# Create Pydantic Model for User Response Endpoint 
class UserResponse(BaseModel):
    id : int
    name : str
    email : EmailStr 

    class Config:
        orm_mode = True


# Create Pydantic Model for User Update Endpoint 
class UserUpdate(BaseModel):
    name : Optional[str] = None
    email : Optional[EmailStr] = None
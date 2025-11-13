from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from database import Base
import logging

logger = logging.getLogger(__name__)

# Create ORM Model for DB
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.debug(f"User ORM model instantiated with email: {kwargs.get('email')}")

# Create Pydantic Model for User Creation Endpoint
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Name must be at least 3 characters")
    email: EmailStr = Field(..., description="Email must be a valid email address")
    password: str = Field(..., min_length=5, description="Password must be at least 5 characters")

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"UserCreate model created for email: {self.email}")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        logger.debug(f"Validating name: {v}")
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        logger.debug("Validating password length")
        if len(v) < 5:
            logger.warning("Password too short during UserCreate validation")
        return v

# Create Pydantic Model for User Response Endpoint
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

    def __init__(self, **data):
        super().__init__(**data)
        logger.debug(f"UserResponse model created for user id: {self.id}")

# Create Pydantic Model for User Update Endpoint
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"UserUpdate model created with data: {data}")

# Create Pydantic Model for Login Endpoint
class LoginIn(BaseModel):
    email: EmailStr = Field(..., description='Enter your email')
    password: str = Field(..., min_length=3, description='Enter your password')

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"LoginIn model created for email: {self.email}")

from sqlalchemy import Column, Integer, String
from database import Base
from logging_config import logger 


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


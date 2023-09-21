from pydantic import BaseModel

class Customer(BaseModel):
    id: str
    name: str
    email: str

from sqlalchemy import Column, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CustomerDB(Base):
    __tablename__ = "customers"

    id = Column(Text, primary_key=True)
    name = Column(Text)
    email = Column(Text)
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from database import Base


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    age = Column(Integer)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    pincode = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    activation_token = Column(String, unique=True)
    is_active = Column(Boolean, default=False)
    profile_photo = Column(String, nullable=True)

    children = relationship("Child", back_populates="parent")


class Child(Base):
    __tablename__ = "children"
    
    child_id  = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date_added = Column(DateTime, default=datetime.utcnow)
    parent_id = Column(Integer, ForeignKey("parents.id"))
    
    parent = relationship("Parent", back_populates="children")
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Department table — FIRST
class Department(Base):
    __tablename__ = "departments"

    id        = Column(Integer, primary_key=True, index=True)
    dept_name = Column(String, unique=True)

    # relationship
    employees = relationship("Employee", back_populates="department")

# Employee table — SECOND
class Employee(Base):
    __tablename__ = "employees"

    id         = Column(Integer, primary_key=True, index=True)
    emp_name   = Column(String)
    salary     = Column(Integer)
    is_active  = Column(Boolean, default=True)
    city       = Column(String, default="unknown")
    dept_id    = Column(Integer, ForeignKey("departments.id"))

    # relationship
    department = relationship("Department", back_populates="employees")

# User table
class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
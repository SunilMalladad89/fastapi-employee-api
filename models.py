from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Employee(Base):
    __tablename__ = "employee_table"
    id         = Column(Integer, primary_key=True, index=True)
    emp_name   = Column(String)
    emp_no     = Column(Integer)
    phone_no   = Column(String)
    department = Column(String)
    role       = Column(String)
    salary     = Column(Integer)
    is_active  = Column(Boolean, default=True)
    city       = Column(String, default="unknown")

# NEW — User table for login
class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)    # stored as hashed password
from pydantic import BaseModel
from typing import Optional, List

# Department schemas
class DepartmentCreate(BaseModel):
    dept_name: str

class DepartmentResponse(BaseModel):
    id:        int
    dept_name: str

    class Config:
        from_attributes = True

# Employee schemas
class EmployeeCreate(BaseModel):
    emp_name:  str
    salary:    int
    is_active: bool = True
    city:      str = "unknown"
    dept_id:   int

class EmployeeResponse(BaseModel):
    id:         int
    emp_name:   str
    salary:     int
    is_active:  bool
    city:       str
    dept_id:    int
    department: Optional[DepartmentResponse] = None

    class Config:
        from_attributes = True

# User schemas
class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str
from pydantic import BaseModel, Field
from typing import Optional

# Employee schemas
class CreateEmployee(BaseModel):
    emp_name:   str
    emp_no:     int
    phone_no:   str = Field(..., min_length=10, max_length=10)
    department: str
    role:       str
    salary:     int
    is_active:  bool = True
    city:       str = "unknown"

class UpdateEmployee(BaseModel):
    emp_name:   Optional[str] = None
    emp_no:     Optional[int] = None
    phone_no:   Optional[str] = None
    department: Optional[str] = None
    role:       Optional[str] = None
    salary:     Optional[int] = None
    is_active:  Optional[bool] = None
    city:       Optional[str] = None

class EmployeeResponse(BaseModel):
    id:         int
    emp_name:   str
    emp_no:     int
    department: str
    role:       str
    is_active:  bool
    city:       str

    class Config:
        from_attributes = True

# NEW — User schemas
class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from database import Base, SessionLocal, engine
from models import Employee, User
from schemas import CreateEmployee, UpdateEmployee, EmployeeResponse, UserCreate, TokenResponse
from auth import hash_password, verify_password, create_token, get_current_user, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

# ─── AUTH ROUTES ───────────────────────────────

# REGISTER — create new user
@app.post('/register', status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(
        username=user.username,
        password=hash_password(user.password)   # hash before saving ✅
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

# LOGIN — get token
@app.post('/login', response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    token = create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# ─── PROTECTED EMPLOYEE ROUTES ─────────────────

# CREATE — protected
@app.post('/employees', response_model=EmployeeResponse, status_code=201)
def create_employee(
    emp: CreateEmployee,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)   # ← protected ✅
):
    new_employee = Employee(**emp.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

# READ ALL — protected
@app.get('/employees', response_model=List[EmployeeResponse], status_code=200)
def get_all_employees(
    sort: str = "asc",
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)   # ← protected ✅
):
    employees = db.query(Employee).limit(limit).all()
    if sort == "desc":
        employees = list(reversed(employees))
    return employees

# READ ONE — protected
@app.get('/employees/{emp_id}', response_model=EmployeeResponse, status_code=200)
def get_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)   # ← protected ✅
):
    employee = db.query(Employee).filter(Employee.id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee {emp_id} not found")
    return employee

# UPDATE — protected
@app.patch('/employees/{emp_id}', response_model=EmployeeResponse, status_code=200)
def update_employee(
    emp_id: int,
    emp: UpdateEmployee,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)   # ← protected ✅
):
    employee = db.query(Employee).filter(Employee.id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee {emp_id} not found")
    for key, value in emp.dict(exclude_none=True).items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

# DELETE — protected
@app.delete('/employees/{emp_id}', status_code=204)
def delete_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)   # ← protected ✅
):
    employee = db.query(Employee).filter(Employee.id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee {emp_id} not found")
    db.delete(employee)
    db.commit()
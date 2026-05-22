from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from database import Base, SessionLocal, engine
from models import Employee, Department, User
from schemas import (
    EmployeeCreate, EmployeeResponse,
    DepartmentCreate, DepartmentResponse,
    UserCreate, TokenResponse
)
from auth import (
    hash_password, verify_password,
    create_token, get_current_user
)

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── AUTH ROUTES ─────────────────────────────────

@app.post('/register', status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post('/login', response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    token = create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# ── DEPARTMENT ROUTES ───────────────────────────

@app.post('/departments', response_model=DepartmentResponse, status_code=201)
def create_department(
    dept: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    existing = db.query(Department).filter(Department.dept_name == dept.dept_name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Department already exists")
    new_dept = Department(**dept.dict())
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

@app.get('/departments', response_model=List[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return db.query(Department).all()

@app.get('/departments/{dept_id}/employees', response_model=List[EmployeeResponse])
def get_dept_employees(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept.employees

# ── EMPLOYEE ROUTES ─────────────────────────────

@app.post('/employees', response_model=EmployeeResponse, status_code=201)
def create_employee(
    emp: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    dept = db.query(Department).filter(Department.id == emp.dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail=f"Department {emp.dept_id} not found")
    new_employee = Employee(**emp.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@app.get('/employees', response_model=List[EmployeeResponse])
def get_all_employees(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return db.query(Employee).all()

@app.get('/employees/{emp_id}', response_model=EmployeeResponse)
def get_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    employee = db.query(Employee).filter(Employee.id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.patch('/employees/{emp_id}', response_model=EmployeeResponse)
def update_employee(
    emp_id: int,
    emp: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    employee = db.query(Employee).filter(Employee.id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in emp.dict().items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

@app.delete('/employees/{emp_id}', status_code=204)
def delete_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    employee = db.query(Employee).filter(Employee.id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
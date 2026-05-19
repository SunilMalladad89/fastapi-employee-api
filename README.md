# FastAPI Employee Management API

A production-ready REST API built with FastAPI, SQLAlchemy, and JWT Authentication.

## Features
- Complete CRUD operations
- JWT Authentication and Authorization
- SQLite Database with SQLAlchemy ORM
- Docker support
- Data validation with Pydantic
- Response filtering with Response Model

## Tech Stack
- FastAPI
- SQLAlchemy
- Pydantic
- JWT (python-jose)
- Docker
- SQLite

## How to Run locally
pip install -r requirements.txt
uvicorn main:app --reload

## How to Run with Docker
docker build -t employee-api .
docker run -d -p 8000:8000 employee-api

## API Endpoints
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /register | Register user | No |
| POST | /login | Get JWT token | No |
| POST | /employees | Create employee | Yes |
| GET | /employees | Get all employees | Yes |
| GET | /employees/{id} | Get one employee | Yes |
| PATCH | /employees/{id} | Update employee | Yes |
| DELETE | /employees/{id} | Delete employee | Yes |

## Test the API
Visit: http://localhost:8000/docs

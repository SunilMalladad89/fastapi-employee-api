from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Old SQLite — commented out
# DATABASE_URL = "sqlite:///./employees.db"

# New PostgreSQL
DATABASE_URL = "postgresql://postgres:sunil123@localhost:5432/employee_db"
#                                      ↑
#                            replace with YOUR password

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
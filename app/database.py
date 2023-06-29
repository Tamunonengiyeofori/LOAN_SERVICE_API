import stringcase
from sqlalchemy.orm import sessionmaker, declarative_mixin, declared_attr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine 
from config import settings
from sqlalchemy import Column, Integer

# SQLALCHEMY_DATABASE_URL =  "postgresql://postgres:22of22in22@localhost:5432/loan_service"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#create a db dependency for creating database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def create_all_tables():
    Base.metadata.create_all(bind=engine)

def drop_all_tables():
    Base.metadata.drop_all(bind=engine)
    
def get_session():
    return SessionLocal

# @declarative_mixin
# class BaseMixin:
#     @declared_attr
#     def __tablename__(cls):
#         name = cls.__tablename__
#         return stringcase.lowercase(stringcase.snakecase(name))
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
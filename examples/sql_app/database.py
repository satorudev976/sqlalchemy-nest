from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_nest import declarative_nested_model_constructor
from sqlalchemy_nest.orm import BaseModel

engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# use sqlalchemy_nest
Base = declarative_base(cls=BaseModel, constructor=declarative_nested_model_constructor)

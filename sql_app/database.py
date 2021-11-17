from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
import os

load_dotenv()

#configuração do banco de dados
SERVER=os.getenv("SERVER")
USER=os.getenv("USER")
PASS=os.getenv("PASS")
DB=os.getenv("DB")
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER}:{PASS}@{SERVER}/{DB}"
print("HERE -> ", SQLALCHEMY_DATABASE_URL)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

if not database_exists(engine.url):
    create_database(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
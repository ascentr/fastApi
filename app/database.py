from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .config import settings

#sqlAlchemy connection string
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname/<database_name>/'

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:amjad@localhost/fastapi'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, sslmode='require' )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Code below is not used as SQL alchemy is used to talk to the db but is saved for reference
#as it allows deploying raw sql to the db
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', database='fastapi', 
#             user='postgres', password='amjad')

#         cursor = conn.cursor()
#         print("Succeffully connected to database")
#         break                

#     except Exception as error:
#         print("Could Not Connect - Error :" , error)
#         time.sleep(2)
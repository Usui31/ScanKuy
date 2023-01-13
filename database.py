from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root@127.0.0.1/scankuy")

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, bind=engine)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./vuln_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:meinesecurepasswd@postgres:5432/app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url="postgresql+psycopg2://postgres:postgres%40BGW@localhost:5432/Trial"
engine=create_engine(db_url)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)


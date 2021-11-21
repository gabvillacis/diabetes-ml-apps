import os
import databases
from sqlalchemy import create_engine

from db.models import metadata

DATABASE_URL = os.getenv("DATABASE_URL", "mysql://gvillacis:Cl4v3Dificil@ls-79464d1618bc9b09dd33cf3224c0c3f5230b1e39.ctu4mfb9xygf.us-east-1.rds.amazonaws.com/diabetes")

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
metadata.create_all(engine)


def get_database() -> databases.Database:
    return database
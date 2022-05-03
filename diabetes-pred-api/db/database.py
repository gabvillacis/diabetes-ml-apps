import os
import databases
from sqlalchemy import create_engine

from db.models import metadata

DATABASE_URL = os.getenv("DATABASE_URL")

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
metadata.create_all(engine)


def get_database() -> databases.Database:
    return database

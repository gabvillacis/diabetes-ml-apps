import os
import databases
from sqlalchemy import create_engine

from db.models import metadata

DATABASE_URL = os.getenv("DATABASE_URL", "mysql://gvillacis:Cl4v3Dificil@ls-e4c651cccf26b8b851edbc4682f58e4321f6b41e.ctu4mfb9xygf.us-east-1.rds.amazonaws.com/diabetes")

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
metadata.create_all(engine)


def get_database() -> databases.Database:
    return database
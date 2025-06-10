# BackEnd/database/init_db.py

from database.postgres import engine
from models.lap import Lap
from database.postgres import Base

print(" Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print(" Done.")

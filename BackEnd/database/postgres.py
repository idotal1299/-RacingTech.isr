# database/postgres.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# טוען משתני סביבה מקובץ .env
load_dotenv()

# משתנה התחברות למסד (ניתן להגדיר גם דרך Docker או AWS)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/racetech")

# יצירת מנוע התחברות
engine = create_engine(DATABASE_URL)

# Session – אובייקט שאיתו עובדים בבקשות
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# בסיס למודלים (User, Lap וכו')
Base = declarative_base()

# Dependency Injection עבור FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

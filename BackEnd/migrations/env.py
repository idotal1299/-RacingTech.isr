# BackEnd/migrations/env.py

import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# ✅ טוען משתני סביבה מתוך קובץ .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# ✅ מוסיף את BackEnd ל-PYTHONPATH כדי לייבא את המודולים
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ ייבוא Base והמודלים שלך
from database.postgres import Base
from models import lap  # תוכל להוסיף גם user, telemetry וכו'

# ✅ הגדרת המטה-דאטה
target_metadata = Base.metadata

# ✅ הגדרת לוגינג
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """מיגרציה במצב offline (ללא DB חי)"""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise Exception("DATABASE_URL not found in environment")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """מיגרציה במצב online עם חיבור למסד"""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise Exception("DATABASE_URL not found in environment")
    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

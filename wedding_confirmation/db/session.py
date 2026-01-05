"""SQL Session."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# BASE_DIR = Path(__file__).resolve().parents[1]
# DATA_DIR = BASE_DIR / "data"
# DATA_DIR.mkdir(exist_ok=True)

# DATABASE_URL = f"sqlite:///{DATA_DIR / 'boda.db'}"

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(os.environ["DATABASE_URL"])

SessionLocal = sessionmaker(bind=engine)

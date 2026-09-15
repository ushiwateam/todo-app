from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}" f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

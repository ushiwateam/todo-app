import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24



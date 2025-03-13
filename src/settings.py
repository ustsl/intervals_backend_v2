import os

from dotenv import load_dotenv
from envparse import Env

env = Env()

load_dotenv()

OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
SERVICE_TOKEN = os.getenv("SERVICE_TOKEN")
SECRET_AUTH_TOKEN = os.getenv("SECRET_AUTH_TOKEN")

DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST")
TEST_DB_NAME = os.getenv("DATABASE_NAME_TEST")


print(f"Database name: {DB_NAME}")
print(f"Database user: {DB_USER}")
print(f"Database host: {DB_HOST}")


print(f"Database name: {TEST_DB_NAME}")


TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{TEST_DB_NAME}",
)


DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
)

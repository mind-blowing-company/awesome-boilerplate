import os
from dotenv import load_dotenv

load_dotenv(".env")

# Misc
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# Database
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")

DATABASE_ENGINE = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Security
SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY")
JWT_ENCODING_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Social auth
LINKEDIN_URL = os.getenv("LINKEDIN_URL")
GOOGLE_URL = os.getenv("GOOGLE_URL")
FACEBOOK_URL = os.getenv("FACEBOOK_URL")

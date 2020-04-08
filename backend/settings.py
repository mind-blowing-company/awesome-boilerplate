import os
from dotenv import load_dotenv

load_dotenv(".env")

# Misc
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# Database
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_ENGINE = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Security
SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY")
JWT_ENCODING_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Social auth
LINKEDIN_URL = "https://api.linkedin.com/v2/me"
GOOGLE_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
FACEBOOK_URL = "https://graph.facebook.com/v6.0/me?fields=id,email"

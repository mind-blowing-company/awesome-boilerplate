import os
from dotenv import load_dotenv

load_dotenv(".env")

# Misc
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# Database
DATABASE_ENGINE = f"sqlite:///{os.path.join(BASE_PATH, 'db.sqlite')}?check_same_thread=False"

# Security
SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY")
JWT_ENCODING_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TOKEN_URL = "/token"

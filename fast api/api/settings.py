import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

password = urllib.parse.quote_plus(os.getenv("POSTGRES_PASSWORD"))

DATABASE_URL = os.getenv("DATABASE_URL")

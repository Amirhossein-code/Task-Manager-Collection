import os

SECRET_KEY = os.getenv("SECRET_KEY")


ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


DATABASE_URL = (
    "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}".format(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        db_name=os.getenv("POSTGRES_DB"),
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
)


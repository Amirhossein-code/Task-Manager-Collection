from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import settings


engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

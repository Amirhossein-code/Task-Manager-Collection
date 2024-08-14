import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

    # Create all tables from the Base metadata
    Base.metadata.create_all(bind=engine)

    # Apply Alembic migrations
    command.upgrade(alembic_cfg, "head")

    yield  # Tests will run after this point

    # Drop all tables after tests are completed

    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


@pytest.fixture
def db_session():
    db = next(override_get_db())
    try:
        yield db
    finally:
        db.close()

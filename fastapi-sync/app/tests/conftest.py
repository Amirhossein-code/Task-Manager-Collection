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


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def db_session():
    db = next(override_get_db())
    try:
        yield db
    finally:
        db.close()


############################################## Common fixtures shared between directories ##############################################
@pytest.fixture
def create_user(client: TestClient):
    def _create_user(
        email: str = "user90@gmail.com",
        password: str = "ILoveFastAPI90@90",
        full_name: str = "halo string",
    ):
        res = client.post(
            "/users/",
            json={
                "email": email,
                "password": password,
                "full_name": full_name,
            },
        )
        return res

    return _create_user


@pytest.fixture
def create_access_token(client: TestClient):
    def _create_token(
        grant_type: str = "password",
        email: str = "user94@gmail.com",
        password: str = "ILoveFastAPI990@90",
        scope: str = "",
        client_id: str = "string",
        client_secret: str = "string",
    ):
        form_data = {
            "grant_type": grant_type,
            "username": email,
            "password": password,
            "scope": scope,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        res = client.post(
            "/auth/token",
            data=form_data,
            headers={
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        return res

    return _create_token


@pytest.fixture
def create_user_with_token(create_user, create_access_token) -> str:
    def _do(
        email: str = "user900@gmail.com",
        password: str = "ILoveFastAPI90@9010",
    ):
        create_user(email=email, password=password)
        res = create_access_token(email=email, password=password)
        response_json = res.json()
        return response_json["access_token"]

    return _do

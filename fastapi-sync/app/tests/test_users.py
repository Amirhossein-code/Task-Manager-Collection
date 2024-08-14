import pytest
from ..models import User
from ..utils.auth.hashing import Hash
from .conftest import apply_migrations, client, db_session  # noqa: F401


class TestUserCreate:
    def test_sign_up_create_user_returns_201(self, db_session):  # noqa: F811
        res = client.post(
            "/users/",
            json={
                "email": "user90@gmail.com",
                "password": "ILoveFastAPI990@90",
                "full_name": "Test Full Name",
            },
        )
        assert res.status_code == 201, res.text
        # Check returned data from the endpoint
        data = res.json()
        assert data["email"] == "user90@gmail.com"
        assert data["full_name"] == "Test Full Name"
        assert data["is_active"]

        user = db_session.query(User).filter(User.email == "user90@gmail.com").first()

        # check record creation
        assert user is not None
        # check password hash
        assert user.hashed_password != "ILoveFastAPI990@90"
        assert Hash.validate_password("ILoveFastAPI990@90", user.hashed_password)

        # check user data from Database
        assert user.email == "user90@gmail.com"
        assert user.full_name == "Test Full Name"
        assert user.is_active
        assert user.created_at is not None
        assert user.last_updated is not None

    @pytest.mark.parametrize(
        "password,expected_error",
        [
            ("", "Password must be at least 8 characters long"),
            ("short", "Password must be at least 8 characters long"),
            (
                "a" * 51,
                "Password must be at most 50 characters long",
            ),
            (
                "noSpecialChar123",
                "Password must contain at least one special character",
            ),
            ("NoNumber!", "Password must contain at least one digit"),
            ("nouppercase1!", "Password must contain at least one uppercase letter"),
            ("NOLOWERCASE1!", "Password must contain at least one lowercase letter"),
        ],
    )
    def test_password_validation_fails_returns_422(
        self,
        db_session,  # noqa: F811
        password: str,
        expected_error: str,
    ):
        res = client.post(
            "/users/",
            json={
                "email": "user91@gmail.com",
                "password": password,
                "full_name": "Test Full Name",
            },
        )
        assert res.status_code == 422, res.text
        response_json = res.json()
        error_messages = [error["msg"] for error in response_json["detail"]]

        assert any(expected_error in msg for msg in error_messages)

        user = db_session.query(User).filter(User.email == "user91@gmail.com").first()
        assert user is None

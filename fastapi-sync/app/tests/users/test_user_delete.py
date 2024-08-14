from ...models import User


class TestUserDelete:
    def test_logged_in_user_deletes_account_returns_204(
        self, client, create_user_with_token, db_session
    ):
        email = "user96@gmail.com"
        password = "TestPassword123!"

        access_token = create_user_with_token(email=email, password=password)

        res = client.delete(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert res.status_code == 204, res.text

        user = db_session.query(User).filter(User.email == email).first()
        assert user is None

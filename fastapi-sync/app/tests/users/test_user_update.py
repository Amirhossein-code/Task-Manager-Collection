import pytest


class TestUserUpdate:
    @pytest.mark.parametrize(
        "method, email",
        [
            ("PUT", "user97@gmail.com"),
            ("PATCH", "user98@gmail.com"),
        ],
    )
    def test_logged_in_user_updates_their_info(
        self,
        client,
        create_user_with_token,
        method: str,
        email: str,
    ):
        full_name = "This is my full name"
        updated_full_name = "New Full Name Updated"

        access_token = create_user_with_token(email=email, full_name=full_name)

        response = client.request(
            method,
            "/users/me",
            json={"full_name": updated_full_name},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # Assert the response
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == updated_full_name
        assert data["full_name"] != full_name

class TestUserRead:
    def test_logged_in_user_gets_back_their_info_returns_200(
        self, client, create_user_with_token
    ):
        email = "user96@gmail.com"
        full_name = "This is my full name"
        access_token = create_user_with_token(email=email, full_name=full_name)
        res = client.get(
            "/users/me", headers={"Authorization": f"Bearer {access_token}"}
        )
        assert res.status_code == 200

        data = res.json()
        assert data["email"] == email
        assert data["full_name"] == full_name
        assert data["is_active"]
        

from ...models import User


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

    def test_logged_in_inactive_user_tries_getting_back_their_info_returns_400(
        self, client, create_user_with_token, db_session, create_access_token
    ):
        # Step 1: Create a user and obtain an access token
        email = "user969@gmail.com"
        password = "90@donER@232md"
        
        create_user_with_token(email=email, password=password)

        # Step 2: Update the user's _is_active field to false
        user = db_session.query(User).filter(User.email == email).first()
        if user:
            user.is_active = False
            db_session.commit()

        response_access_token = create_access_token(email=email, password=password)
        response_access_token_json = response_access_token.json()
        in_active_access_token = response_access_token_json["access_token"]

        # Step 3: Try accessing the user's information again
        res = client.get(
            "/users/me", headers={"Authorization": f"Bearer {in_active_access_token}"}
        )

        # Step 4: Assert that the response returns a 400 status code
        assert res.status_code == 400
        assert res.json() == {"detail": "Inactive user"}

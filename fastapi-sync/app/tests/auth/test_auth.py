def test_create_access_token_returns_200(client, create_user, create_access_token):
    create_user(
        email="user94@gmail.com",
        password="ILoveFastAPI990@90",
    )

    res = create_access_token(
        email="user94@gmail.com",
        password="ILoveFastAPI990@90",
    )

    assert res.status_code == 200

    response_json = res.json()
    assert "access_token" in response_json
    assert "token_type" in response_json


def test_create_access_token_without_existing_user_returns_401(
    create_access_token,
):
    res = create_access_token(
        email="user94592034570234@gmail.com",
        password="ILoveFastAPI990@90",
    )

    assert res.status_code == 401
